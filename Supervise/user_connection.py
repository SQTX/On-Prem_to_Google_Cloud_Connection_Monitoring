

from supervisor import SupervisingDNS, SupervisingISP, SupervisingRouter

class UserConnectionInspector():

    def __init__(self, dns_ip_address, isp_ip_address, router_ip_address):
        self.dns_ip_address = dns_ip_address
        self.isp_ip_address = isp_ip_address
        self.router_ip_address = router_ip_address

    
    