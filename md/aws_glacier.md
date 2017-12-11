##aws cli for glacier

1. create vaulet
```bash
$ aws glacier create-vault --account-id - --vault-name myvault
{
    "location": "/123456789012/vaults/myvault"
}
```

2. list vaulet
```bash
aws glacier list-vaults --account-id -
```

The AccountId value is the AWS account ID. This value must match the AWS account ID associated with the credentials used to sign the request. You can either specify an AWS account ID or optionally a single '- ' (hyphen), in which case Amazon Glacier uses the AWS account ID associated with the credentials used to sign the request. If you specify your account ID, do not include any hyphens ('-') in the ID.

Output
```json
{
    "VaultList": [
        {
            "VaultName": "ub1.flight.glacier",
            "VaultARN": "arn:aws:glacier:ap-southeast-2:718584735217:vaults/ub1.flight.glacier",
            "CreationDate": "2017-12-11T05:00:26.105Z",
            "NumberOfArchives": 0,
            "SizeInBytes": 0
        }
    ]
}
```

3. Upload one archive file
```bash
aws glacier upload-archive --account-id - --vault-name my-vault --body archive.zip
```
Output
```json
{
    "archiveId": "kKB7ymWJVpPSwhGP6ycSOAekp9ZYe_--zM_mw6k76ZFGEIWQX-ybtRDvc2VkPSDtfKmQrj0IRQLSGsNuDp-AJVlu2ccmDSyDUmZwKbwbpAdGATGDiB3hHO0bjbGehXTcApVud_wyDw",
    "checksum": "969fb39823836d81f0cc028195fcdbcbbe76cdde932d4646fa7de5f21e18aa67",
    "location": "/0123456789012/vaults/my-vault/archives/kKB7ymWJVpPSwhGP6ycSOAekp9ZYe_--zM_mw6k76ZFGEIWQX-ybtRDvc2VkPSDtfKmQrj0IRQLSGsNuDp-AJVlu2ccmDSyDUmZwKbwbpAdGATGDiB3hHO0bjbGehXTcApVud_wyDw"
}
```



### reference
1. AWS cli for glacier
http://docs.aws.amazon.com/cli/latest/reference/glacier/index.html
2. using example 
http://docs.aws.amazon.com/cli/latest/userguide/cli-using-glacier.html