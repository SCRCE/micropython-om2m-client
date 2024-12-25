class AE:
    """
    Application Entity resource model.
    """
    def __init__(self, rn: str, api: str, rr: bool = False, lbl=None, aei: str = None):
        self.rn = rn                     # resource name
        self.api = api                   # application ID
        self.rr = rr                     # request reachability
        self.lbl = lbl or []             # labels (default: empty list)
        self.aei = aei                   # AE-ID assigned by the CSE after creation


class Container:
    """
    Container resource model.
    """
    def __init__(self, rn: str, lbl=None, cni: int = 0, cbs: int = 0):
        self.rn = rn                     # resource name
        self.lbl = lbl or []             # labels (default: empty list)
        self.cni = cni                   # current number of instances
        self.cbs = cbs                   # current byte size


class ContentInstance:
    """
    Content Instance resource model.
    """
    def __init__(self, cnf: str, con: str, rn: str = None):
        self.cnf = cnf                   # content format
        self.con = con                   # content
        self.rn = rn                     # resource name (optional)


class Subscription:
    """
    Subscription resource model.
    """
    def __init__(self, rn: str, nu: str, nct: int = 2):
        self.rn = rn                     # resource name
        self.nu = nu                     # notification URI
        self.nct = nct                   # notification content type (default: 2)
