{
  "name": "Advanced Multilingual AI Workflow",
  "nodes": [
    {
      "parameters": {
        "updates": ["message"],
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.telegramTrigger",
      "typeVersion": 1.1,
      "position": [-520, 580],
      "id": "bc887879-2488-4dff-bdcd-602e53ea6784",
      "name": "Receive Message",
      "webhookId": "97ad91b8-8d3c-4c40-b197-bd5e509538ba",
      "credentials": {
        "telegramApi": {
          "id": "Nmm8Wn3O3LmE663r",
          "name": "Telegram account"
        }
      }
    },
    {
      "parameters": {
        "operation": "detect",
        "text": "={{ $json.message.text || $json.message.caption || '' }}",
        "options": {
          "fallbackLanguage": "en-US",
          "supportedLanguages": [
            "af", "az", "bs", "ca", "cs", "cy", "da", "de", "et", "en-GB", "en-US", "es-ES", "es-LA", "eu", "fil", "fr-CA", "fr-FR", "ga", "gl", "hr", "id", "zu", "is", "it", "sw", "lv", "lt", "hu", "ms", "nl", "no", "uz", "pl", "pt-BR", "pt-PT", "ro", "sq", "sk", "sl", "sr-Latn", "fi", "sv", "vi", "tr", "el", "be", "bg", "ky", "kk", "mk", "mn", "ru", "sr-Cyrl", "uk", "ka", "hy", "he", "ur", "ar", "fa", "am", "ne", "mr", "hi", "as", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "th", "lo", "my", "km", "ko", "zh-HK", "ja", "zh-CN", "zh-TW"
          ]
        }
      },
      "type": "n8n-nodes-base.languageDetector",
      "typeVersion": 1.0,
      "position": [-320, 580],
      "id": "lang-detect-001",
      "name": "Detect Language"
    },
    {
      "parameters": {
        "operation": "verify",
        "type": "reCAPTCHA-v3",
        "siteKey": "YOUR_RECAPTCHA_SITE_KEY",
        "secretKey": "YOUR_RECAPTCHA_SECRET_KEY",
        "options": {
          "scoreThreshold": 0.5,
          "language": "={{ $node['Detect Language'].json.detectedLanguage }}"
        }
      },
      "type": "n8n-nodes-base.captcha",
      "typeVersion": 1.0,
      "position": [-320, 780],
      "id": "captcha-001",
      "name": "CAPTCHA Verification"
    },
    {
      "parameters": {
        "rules": {
          "values": [
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "leftValue": "={{ $json.message.photo }}",
                    "rightValue": "",
                    "operator": {
                      "type": "array",
                      "operation": "exists",
                      "singleValue": true
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "image"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "leftValue": "={{ $json.message.voice.file_id }}",
                    "rightValue": "",
                    "operator": {
                      "type": "string",
                      "operation": "exists",
                      "singleValue": true
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "voice"
            },
            {
              "conditions": {
                "options": {
                  "caseSensitive": true,
                  "typeValidation": "strict",
                  "version": 2
                },
                "conditions": [
                  {
                    "leftValue": "={{ $json.message.text }}",
                    "rightValue": "",
                    "operator": {
                      "type": "string",
                      "operation": "exists",
                      "singleValue": true
                    }
                  }
                ],
                "combinator": "and"
              },
              "renameOutput": true,
              "outputKey": "text"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3.2,
      "position": [-120, 580],
      "id": "2df6de05-cdc8-4e9a-8955-46ddc4c25824",
      "name": "Switch"
    },
    {
      "parameters": {
        "resource": "file",
        "fileId": "={{ $json.message.photo[2].file_id }}"
      },
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [80, 60],
      "id": "61744e05-c3e7-46f4-93a0-b853f5297299",
      "name": "Download Image",
      "webhookId": "4404a756-41e5-4497-82ed-dc79427faedc",
      "credentials": {
        "telegramApi": {
          "id": "tvQadz3AzgHOG5b8",
          "name": "Telegram account 3"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "const inputItem = items[0];\nconst extension = inputItem.binary.data.fileExtension;\ninputItem.binary.data.mimeType = `image/${extension}`;\nreturn inputItem;"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [260, 60],
      "id": "ebb0a28e-bf53-4fc0-a176-91a9ff143f2c",
      "name": "Fix File Extension"
    },
    {
      "parameters": {
        "resource": "file",
        "fileId": "={{ $json.message.voice.file_id }}"
      },
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [80, 380],
      "id": "ed06330d-1acd-4579-9b0b-4b42793361cf",
      "name": "Get Audio File",
      "webhookId": "ea977965-cb53-4034-afcc-5850b78cf8d6",
      "credentials": {
        "telegramApi": {
          "id": "DEYZvmWxvWNANWdw",
          "name": "Telegram account 2"
        }
      }
    },
    {
      "parameters": {
        "resource": "audio",
        "operation": "transcribe",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "typeVersion": 1.8,
      "position": [260, 380],
      "id": "2b2f3e96-765f-4eff-bd51-cba5f480168f",
      "name": "Transcribe",
      "credentials": {
        "openAiApi": {
          "id": "tVZ6kSbAeaPLUZVP",
          "name": "OpenAi account 2"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "88cbdd27-f094-458b-878f-60504b8c3ad7",
              "name": "text",
              "value": "={{ $json.message.text || $json.transcription || '' }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [80, 640],
      "id": "acb18fb5-e4a8-44d0-8cba-cb2bcb7ae72f",
      "name": "Agent Input"
    },
    {
      "parameters": {
        "promptType": "define",
        "text": "={{ $json.text }}",
        "options": {
          "systemMessage": "=# ROLE\nYou are a helpful assistant named Sam. Respond in a friendly, helpful tone in the user's language: {{ $node['Detect Language'].json.detectedLanguage }}.\n\n# Important Information\nYou are speaking to {{ $('Switch').item.json.message.from.first_name }}.\nCurrent date and time: {{ $now }}.\n\n# Tools\n## Get Emails\nRetrieve unread emails from Gmail. Provide:\n- Summary of body content\n- From email address\n- Sender name\n\n## Send Email\nSend an email with recipient address, subject, and body.\n\n## Get Calendar\nRetrieve calendar events.\n\n## Set Calendar\nCreate new calendar events.\n\n## Contacts\nRetrieve contact information (e.g., email addresses).\n\n## Products list\nCheck inventory or product counts.\n\n## CAPTCHA Verification\nIf user verification is needed, trigger CAPTCHA in the user's language."
        }
      },
      "type": "@n8n/n8n-nodes-langchain.agent",
      "typeVersion": 1.7,
      "position": [640, 440],
      "id": "8684a559-7bd5-45eb-b7c7-954346e1f61f",
      "name": "AI Agent",
      "credentials": {
        "xaiApi": {
          "id": "xai-grok3-001",
          "name": "xAI Grok 3 account"
        }
      }
    },
    {
      "parameters": {
        "sessionIdType": "customKey",
        "sessionKey": "{{ $('Receive Message').item.json.message.chat.id }}",
        "contextWindowLength": 20,
        "cache": {
          "type": "redis",
          "connection": "redis://localhost:6379"
        }
      },
      "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
      "typeVersion": 1.3,
      "position": [840, 660],
      "id": "98a47480-7018-449d-9eb0-ebdf1da31614",
      "name": "Window Buffer Memory"
    },
    {
     33      "parameters": {
        "resource": "image",
        "operation": "analyze",
        "modelId": "grok-3-vision",
        "text": "={{ $('Receive Message').item.json.message.caption || \"Describe this image in {{ $node['Detect Language'].json.detectedLanguage }}\" }}",
        "inputType": "base64",
        "options": {}
      },
      "type": "@n8n/n8n-nodes-langchain.xai",
      "typeVersion": 1.0,
      "position": [420, 60],
      "id": "62fdbbc8-a367-4b17-b480-a393e17bee6f",
      "name": "Analyze Image",
      "credentials": {
        "xaiApi": {
          "id": "xai-grok3-001",
          "name": "xAI Grok 3 account"
        }
      }
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "ec3a884f-480f-4462-9437-a7de0faed372",
              "name": "output",
              "value": "={{ $json.content }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      },
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [580, 60],
      "id": "a25375a2-c2fa-4fa6-bd56-019b85df5bb0",
      "name": "Format Output"
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "typeValidation": "strict",
            "version": 2
          },
          "conditions": [
            {
              "leftValue": "={{ $('Receive Message').item.json.message.voice.file_id }}",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "exists",
                "singleValue": true
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "type": "n8n-nodes-base.if",
      "typeVersion": 2.2,
      "position": [1100, 320],
      "id": "86a2ec1b-ba10-4d06-bf47-476a9842a300",
      "name": "Audio Response?"
    },
    {
      "parameters": {
        "resource": "audio",
        "input": "={{ $json.output }}",
        "voice": "nova",
        "options": {
          "language": "={{ $node['Detect Language'].json.detectedLanguage }}"
        }
      },
      "type": "@n8n/n8n-nodes-langchain.xai",
      "typeVersion": 1.0,
      "position": [1340, 220],
      "id": "c9a6ec50-736b-4b8e-b459-2bbc1460b688",
      "name": "Generate Audio",
      "credentials": {
        "xaiApi": {
          "id": "xai-grok3-001",
          "name": "xAI Grok 3 account"
        }
      }
    },
    {
      "parameters": {
        "operation": "sendAudio",
        "chatId": "={{ $('Receive Message').item.json.message.chat.id }}",
        "binaryData": true,
        "additionalFields": {}
      },
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [1560, 220],
      "id": "be9bd58a-1aa4-4102-a6a4-515b84e97676",
      "name": "Audio Response",
      "webhookId": "8d5d057f-41e8-4402-9da8-956f48c2122a",
      "credentials": {
        "telegramApi": {
          "id": "ulQJKRGDMDuh0toE",
          "name": "Telegram account 5"
        }
      }
    },
    {
      "parameters": {
        "chatId": "={{ $('Receive Message').item.json.message.chat.id }}",
        "text": "={{ $json.output }}",
        "additionalFields": {
          "appendAttribution": false,
          "replyMarkup": {
            "inline_keyboard": [
              [
                { "text": "Check Emails", "callback_data": "get_emails" },
                { "text": "View Calendar", "callback_data": "get_calendar" }
              ]
            ]
          }
        }
      },
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.2,
      "position": [1340, 440],
      "id": "699d2b50-e532-49dd-a28d-e0e2064ff246",
      "name": "Text Response",
      "webhookId": "5805eda3-1f85-444a-9f23-66e2383f0d4f",
      "credentials": {
        "telegramApi": {
          "id": "OoCYNDRRZZvtl5bc",
          "name": "Telegram account 4"
        }
      }
    },
    {
      "parameters": {
        "operation": "authenticate",
        "scopes": ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail"],
        "options": {
          "guestMode": true,
          "privateBrowsing": true
        }
      },
      "type": "n8n-nodes-base.googleOAuth2",
      "typeVersion": 1.0,
      "position": [-320, 980],
      "id": "google-auth-001",
      "name": "Google Auth",
      "credentials": {
        "googleOAuth2Api": {
          "id": "google-oauth2-001",
          "name": "Google OAuth2 account"
        }
      }
    },
    {
      "parameters": {
        "sendTo": "={{ $fromAI('recipient_email') }}",
        "subject": "={{ $fromAI('email_subject') }}",
        "emailType": "text",
        "message": "={{ $fromAI('email_body') }}",
        "options": {
          "appendAttribution": false
        }
      },
      "type": "n8n-nodes-base.gmailTool",
      "typeVersion": 2.1,
      "position": [360, 1060],
      "id": "270a0975-a963-4d52-8b4c-f75ca04450aa",
      "name": "Send Email",
      "webhookId": "33501ace-0ca0-44b3-b91b-bdb370df8401",
      "credentials": {
        "gmailOAuth2": {
          "id": "ZU1RfaB3DP956GqM",
          "name": "Gmail account"
        }
      }
    },
    {
      "parameters": {
        "calendar": {
          "__rl": true,
          "value": "the.maryam.sadeghi@gmail.com",
          "mode": "list",
          "cachedResultName": "the.maryam.sadeghi@gmail.com"
        },
        "start": "={{ $fromAI('start', \"Date and time when the event should start\") }}",
        "end": "={{ $fromAI('end', \"Date and time when the event should end\") }}",
        "additionalFields": {
          "description": "={{ $fromAI('description', \"Description of the event\") }}",
          "summary": "={{ $fromAI('title', \"Title of the event\") }}"
        }
      },
      "type": "n8n-nodes-base.googleCalendarTool",
      "typeVersion": 1.3,
      "position": [500, 1060],
      "id": "076fb38f-a92e-4a82-9367-a27df7dcdf25",
      "name": "Set Calendar",
      "credentials": {
        "googleCalendarOAuth2Api": {
          "id": "6jmpRvBbrRJ24wao",
          "name": "Google Calendar account 2"
        }
      }
    },
    {
      "parameters": {
        "documentId": {
          "__rl": true,
          "value": "1cwEf7LqPbhloIrw4laehi__aAmtWbWJsPPiNkn9HW9A",
          "mode": "list",
          "cachedResultName": "contact_emails",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1cwEf7LqPbhloIrw4laehi__aAmtWbWJsPPiNkn9HW9A/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "Sheet1",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1cwEf7LqPbhloIrw4laehi__aAmtWbWJsPPiNkn9HW9A/edit#gid=0"
        },
        "options": {
          "cache": {
            "ttl": 3600
          }
        }
      },
      "type": "n8n-nodes-base.googleSheetsTool",
      "typeVersion": 4.5,
      "position": [820, 1060],
      "id": "e7181673-52b8-479a-ab12-60a4f977593e",
      "name": "Contacts",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "hwg32RPJCbQg6qOB",
          "name": "Google Sheets account 2"
        }
      }
    },
    {
      "parameters": {
        "documentId": {
          "__rl": true,
          "value": "1cOv3HcE0Sl5hHZ3yF3C1uoazgiURlH_6MZ0p_WbYczs",
          "mode": "list",
          "cachedResultName": "product_list",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1cOv3HcE0Sl5hHZ3yF3C1uoazgiURlH_6MZ0p_WbYczs/edit?usp=drivesdk"
        },
        "sheetName": {
          "__rl": true,
          "value": "gid=0",
          "mode": "list",
          "cachedResultName": "Sheet1",
          "cachedResultUrl": "https://docs.google.com/spreadsheets/d/1cOv3HcE0Sl5hHZ3yF3C1uoazgiURlH_6MZ0p_WbYczs/edit#gid=0"
        },
        "options": {
          "cache": {
            "ttl": 3600
          }
        }
      },
      "type": "n8n-nodes-base.googleSheetsTool",
      "typeVersion": 4.5,
      "position": [660, 1060],
      "id": "ab965d4a-a844-49d0-9967-98ce4c8a5b0c",
      "name": "Products list",
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "1yIiJHv9LCzKRBFv",
          "name": "Google Sheets account"
        }
      }
    },
    {
      "parameters": {
        "content": "## AI Agent with Multilingual Support",
        "height": 460,
        "width": 380
      },
      "type": "n8n-nodes-base.stickyNote",
      "typeVersion": 1,
      "position": [580, 360],
      "id": "81339c66-c353-4c98-95e8-af5555359a95",
      "name": "Sticky Note5"
    }
  ],
  "pinData": {},
  "connections": {
    "Receive Message": {
      "main": [
        [
          {
            "node": "Detect Language",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Detect Language": {
      "main": [
        [
          {
            "node": "CAPTCHA Verification",
            "type": "main",
            "index": 0
          },
          {
            "node": "Switch",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "CAPTCHA Verification": {
      "main": [
        [
          {
            "node": "Google Auth",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Google Auth": {
      "main": [
        [
          {
            "node": "Switch",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Switch": {
      "main": [
        [
          {
            "node": "Download Image",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Get Audio File",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Agent Input",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Download Image": {
      "main": [
        [
jus          {
            "node": "Fix File Extension",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fix File Extension": {
      "main": [
        [
          {
            "node": "Analyze Image",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Analyze Image": {
      "main": [
        [
          {
            "node": "Format Output",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Format Output": {
      "main": [
        [
          {
            "node": "Text Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Get Audio File": {
      "main": [
        [
          {
            "node": "Transcribe",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Transcribe": {
      "main": [
        [
          {
            "node": "Agent Input",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Agent Input": {
      "main": [
        [
          {
            "node": "AI Agent",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "AI Agent": {
      "main": [
        [
          {
            "node": "Audio Response?",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Audio Response?": {
      "main": [
        [
          {
            "node": "Generate Audio",
            "type": "main",
            "index": 0
          }
        ],
        [
          {
            "node": "Text Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Generate Audio": {
      "main": [
        [
          {
            "node": "Audio Response",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Send Email": {
      "ai_tool": [
        [
          {
            "node": "AI Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    },
    "Set Calendar": {
      "ai_tool": [
        [
          {
            "node": "AI Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    },
    "Window Buffer Memory": {
      "ai_memory": [
        [
          {
            "node": "AI Agent",
            "type": "ai_memory",
            "index": 0
          }
        ]
      ]
    },
    "Contacts": {
      "ai_tool": [
        [
          {
            "node": "AI Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    },
    "Products list": {
      "ai_tool": [
        [
          {
            "node": "AI Agent",
            "type": "ai_tool",
            "index": 0
          }
        ]
      ]
    }
  ],
  "active": true,
  "settings": {
    "executionOrder": "v1",
    "errorHandling": {
      "retryOnFail": {
        "maxAttempts": 3,
        "waitBetween": 1000
      }
    }
  },
  "versionId": "64f27f4e-7af0-4f35-94b4-037265825201",
  "meta": {
    "templateCredsSetupCompleted": true,
    "instanceId": "a4655248a9f69a44c95c27f9040f496c667d2f4d476552046fe4b21ef917f17b"
  },
  "id": "2EEIJMegHhLhkhUA",
  "tags": ["multilingual", "AI", "telegram", "automation"]
}
