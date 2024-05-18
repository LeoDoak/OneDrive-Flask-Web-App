from OpenSSL.crypto import X509, X509Extension


class CertificateBase:
    def __init__(self, *, certificate: X509 = None):
        self.certificate = certificate or X509()

    def basicConstraints(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Basic-Constraints
        self.certificate.add_extensions([
            X509Extension(b"basicConstraints", *args, **kwargs),
        ])

    def subjectAltName(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Key-Usage
        self.certificate.add_extensions([
            X509Extension(b"subjectAltName", *args, **kwargs),
        ])

    def keyUsage(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Extended-Key-Usage
        self.certificate.add_extensions([
            X509Extension(b"keyUsage", *args, **kwargs),
        ])

    def extendedKeyUsage(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Subject-Key-Identifier
        self.certificate.add_extensions([
            X509Extension(b"extendedKeyUsage", *args, **kwargs),
        ])

    def subjectKeyIdentifier(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Authority-Key-Identifier
        self.certificate.add_extensions([
            X509Extension(b"subjectKeyIdentifier", *args, **kwargs),
        ])

    def authorityKeyIdentifier(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Subject-Alternative-Name
        self.certificate.add_extensions([
            X509Extension(b"authorityKeyIdentifier", *args, **kwargs),
        ])

    def issuerAltName(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Issuer-Alternative-Name
        self.certificate.add_extensions([
            X509Extension(b"issuerAltName", *args, **kwargs),
        ])

    def authorityInfoAccess(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Authority-Info-Access
        self.certificate.add_extensions([
            X509Extension(b"authorityInfoAccess", *args, **kwargs),
        ])

    def crlDistributionPoints(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#CRL-distribution-points
        self.certificate.add_extensions([
            X509Extension(b"crlDistributionPoints", *args, **kwargs),
        ])

    def issuingDistributionPoint(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Issuing-Distribution-Point
        self.certificate.add_extensions([
            X509Extension(b"issuingDistributionPoint", *args, **kwargs),
        ])

    def certificatePolicies(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Certificate-Policies
        self.certificate.add_extensions([
            X509Extension(b"certificatePolicies", *args, **kwargs),
        ])

    def policyConstraints(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Policy-Constraints
        self.certificate.add_extensions([
            X509Extension(b"policyConstraints", *args, **kwargs),
        ])

    def inhibitAnyPolicy(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Inhibit-Any-Policy
        self.certificate.add_extensions([
            X509Extension(b"inhibitAnyPolicy", *args, **kwargs),
        ])

    def nameConstraints(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#Name-Constraints
        self.certificate.add_extensions([
            X509Extension(b"nameConstraints", *args, **kwargs),
        ])

    def noCheck(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#OCSP-No-Check
        self.certificate.add_extensions([
            X509Extension(b"noCheck", *args, **kwargs),
        ])

    def tlsfeature(self, *args, **kwargs):
        # https://www.openssl.org/docs/manmaster/man5/x509v3_config.html#TLS-Feature-aka-Must-Staple
        self.certificate.add_extensions([
            X509Extension(b"tlsfeature", *args, **kwargs),
        ])


