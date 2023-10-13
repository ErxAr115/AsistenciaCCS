# Asistencia CCS

## Plantilla de mensaje
```
{
  "object": "whatsapp_business_account",
  "entry": [{
      "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
      "changes": [{
          "value": {
              "messaging_product": "whatsapp",
              "metadata": {
                  "display_phone_number": "PHONE_NUMBER",
                  "phone_number_id": "PHONE_NUMBER_ID"
              },
              "contacts": [{
                  "profile": {
                    "name": "NAME"
                  },
                  "wa_id": "PHONE_NUMBER"
                }],
              "messages": [{
                  "from": 526677263734,
                  "id": "wamid.ID",
                  "timestamp": "TIMESTAMP",
                  "text": {
                    "body": "horarios de atención"
                  },
                  "type": "text"
                }]
          },
          "field": "messages"
        }]
  }]
}
```
