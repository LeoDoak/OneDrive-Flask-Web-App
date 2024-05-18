# Easy RSA

<badges>[![version](https://img.shields.io/pypi/v/easyrsa.svg)](https://pypi.org/project/easyrsa/)
[![license](https://img.shields.io/pypi/l/easyrsa.svg)](https://pypi.org/project/easyrsa/)
[![pyversions](https://img.shields.io/pypi/pyversions/easyrsa.svg)](https://pypi.org/project/easyrsa/)  
[![powered](https://img.shields.io/badge/Say-Thanks-ddddff.svg)](https://saythanks.io/to/foxe6)
[![donate](https://img.shields.io/badge/Donate-Paypal-0070ba.svg)](https://paypal.me/foxe6)
[![made](https://img.shields.io/badge/Made%20with-PyCharm-red.svg)](https://paypal.me/foxe6)
</badges>

<i>Encrypt symmetric keys with RSA. Create self-signed certificates.</i>

# Hierarchy

```
easyrsa
|---- EasyRSA()
|   |---- gen_key_pair()
|   |---- encrypt()
|   |---- decrypt()
|   |---- sign()
|   |---- verify()
|   '---- max_msg_size()
|---- Certificate()
|   |---- dump()
|   |---- basicConstraints()
|   |---- subjectAltName()
|   |---- keyUsage()
|   |---- extendedKeyUsage()
|   |---- subjectKeyIdentifier()
|   |---- authorityKeyIdentifier()
|   |---- issuerAltName()
|   |---- authorityInfoAccess()
|   |---- crlDistributionPoints()
|   |---- issuingDistributionPoint()
|   |---- certificatePolicies()
|   |---- policyConstraints()
|   |---- inhibitAnyPolicy()
|   |---- nameConstraints()
|   |---- noCheck()
|   '---- tlsfeature()
|---- CertificateAuthority()
|   |---- sign()
|   |---- dump()
|   |---- sign_certificate()
|   |---- verify_certificate()
|   |---- verify_certificate_from_raw()
|   |---- basicConstraints()
|   |---- subjectAltName()
|   |---- keyUsage()
|   |---- extendedKeyUsage()
|   |---- subjectKeyIdentifier()
|   |---- authorityKeyIdentifier()
|   |---- issuerAltName()
|   |---- authorityInfoAccess()
|   |---- crlDistributionPoints()
|   |---- issuingDistributionPoint()
|   |---- certificatePolicies()
|   |---- policyConstraints()
|   |---- inhibitAnyPolicy()
|   |---- nameConstraints()
|   |---- noCheck()
|   '---- tlsfeature()
'---- EasyRSAv1()
    |---- gen_key_pair()
    |---- encrypt()
    |---- decrypt()
    |---- sign()
    |---- verify()
    '---- max_msg_size()
```

# Example

## python
See `test`.