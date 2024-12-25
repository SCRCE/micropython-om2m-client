try:
    import urequests as requests
except ImportError:
    import requests

from .models import AE, Container, ContentInstance, Subscription
from .exceptions import OM2MRequestError


class OM2MClient:
    def __init__(
        self,
        base_url: str,
        cse_id: str,
        cse_name: str,
        username: str,
        password: str,
        use_json: bool = True
    ):
        self.base_url = base_url.rstrip("/")
        self.cse_id = cse_id
        self.cse_name = cse_name
        self.username = username
        self.password = password
        self.use_json = use_json
        self._common_headers = {
            "X-M2M-Origin": f"{self.username}:{self.password}",
        }

    def _make_url(self, relative_path: str) -> str:
        """
        Construct the correct URL from a given resource path.
        For oneM2M, some paths might be prefixed by '~'; if so, adapt the final URL accordingly.
        """
        rp = relative_path.strip("/")
        if rp.startswith("~"):
            return f"{self.base_url}/{rp.lstrip('~')}"
        return f"{self.base_url}/~/{rp}"

    def _content_headers(self, resource_type: int):
        """
        Returns the Content-Type and Accept headers based on whether JSON or XML is used,
        as well as the resource type (ty).
        """
        common_headers = self._common_headers.copy()
        content_type = f"application/json;ty={resource_type}" if self.use_json else f"application/xml;ty={resource_type}"
        accept_type = "application/json" if self.use_json else "application/xml"

        headers = common_headers
        headers["Content-Type"] = content_type
        headers["Accept"] = accept_type

        return headers

    def _request(self, method: str, url: str, headers=None, data=None):
        """
        A wrapper around requests or urequests that handles exceptions
        and ensures compatibility with both libraries.
        """
        try:
            method = method.lower()
            if method == "get":
                resp = requests.get(url, headers=headers)
            elif method == "post":
                resp = requests.post(url, headers=headers, data=data)
            elif method == "put":
                resp = requests.put(url, headers=headers, data=data)
            elif method == "delete":
                resp = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
        except Exception as exc:
            raise OM2MRequestError(f"Request to {url} failed: {exc}") from exc

        if not (200 <= resp.status_code < 300):
            raise OM2MRequestError(
                f"HTTP {resp.status_code} Error for {url}:\n{resp.text}"
            )

        return resp

    def retrieve_resource(self, resource_path: str) -> str:
        """
        Retrieve a resource from the CSE (oneM2M GET operation).
        """
        url = self._make_url(resource_path)
        headers = self._common_headers.copy()
        headers["Accept"] = "application/json" if self.use_json else "application/xml"
        resp = self._request("GET", url, headers=headers)
        return resp.text

    def create_ae(self, ae: AE) -> str:
        """
        Create an Application Entity (AE) under the CSE.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(self.cse_id)
        headers = self._content_headers(2)  # AE resource type
        if self.use_json:
            import json
            body = {
                "m2m:ae": {
                    "rn": ae.rn,
                    "api": ae.api,
                    "rr": str(ae.rr).lower(),
                    "lbl": ae.lbl
                }
            }
            data = json.dumps(body)
        else:
            label_text = " ".join(ae.lbl) if ae.lbl else ""
            data = f"""<m2m:ae xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{ae.rn}">
    <api>{ae.api}</api>
    <rr>{"true" if ae.rr else "false"}</rr>
    <lbl>{label_text}</lbl>
</m2m:ae>"""
        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_container(self, parent_path: str, container: Container) -> str:
        """
        Create a Container resource (CNT) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(3)  # Container resource type
        if self.use_json:
            import json
            body = {
                "m2m:cnt": {
                    "rn": container.rn,
                    "lbl": container.lbl
                }
            }
            data = json.dumps(body)
        else:
            label_text = " ".join(container.lbl) if container.lbl else ""
            data = f"""<m2m:cnt xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{container.rn}">
    <lbl>{label_text}</lbl>
</m2m:cnt>"""
        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_content_instance(self, parent_path: str, cin: ContentInstance) -> str:
        """
        Create a ContentInstance resource (CIN) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(4)  # ContentInstance resource type
        if self.use_json:
            import json
            body = {
                "m2m:cin": {
                    "cnf": cin.cnf,
                    "con": cin.con
                }
            }
            if cin.rn:
                body["m2m:cin"]["rn"] = cin.rn
            data = json.dumps(body)
        else:
            rn_attr = f' rn="{cin.rn}"' if cin.rn else ""
            data = f"""<m2m:cin xmlns:m2m="http://www.onem2m.org/xml/protocols"{rn_attr}>
    <cnf>{cin.cnf}</cnf>
    <con>{cin.con}</con>
</m2m:cin>"""
        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")

    def create_subscription(self, parent_path: str, subscription: Subscription) -> str:
        """
        Create a Subscription resource (SUB) under a given parent path.
        Returns the 'Content-Location' of the created resource.
        """
        url = self._make_url(parent_path)
        headers = self._content_headers(23)  # Subscription resource type
        if self.use_json:
            import json
            body = {
                "m2m:sub": {
                    "rn": subscription.rn,
                    "nu": [subscription.nu],
                    "nct": subscription.nct
                }
            }
            data = json.dumps(body)
        else:
            data = f"""<m2m:sub xmlns:m2m="http://www.onem2m.org/xml/protocols" rn="{subscription.rn}">
    <nu>{subscription.nu}</nu>
    <nct>{subscription.nct}</nct>
</m2m:sub>"""
        resp = self._request("POST", url, headers=headers, data=data)
        return resp.headers.get("Content-Location", "")
