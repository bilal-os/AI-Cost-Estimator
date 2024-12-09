from datetime import datetime, timedelta

MOCK_PROJECTS = [
    {
        "projectName": "Inventory Manager",
        "dateCreated": (datetime.now() - timedelta(days=30)).isoformat(),
        "functionPointAnalysis": {
            "externalInputs": {
                "count": 3,
                "modules": ["Login form", "Customer entry", "File upload"]
            },
            "externalOutputs": {
                "count": 2,
                "modules": ["Order confirmation", "Sales report"]
            },
            "externalInquiries": {
                "count": 1,
                "modules": ["Product search"]
            },
            "internalLogicalFiles": {
                "count": 2,
                "modules": ["Employee records", "Product catalog"]
            },
            "externalInterfaceFiles": {
                "count": 1,
                "modules": ["Currency exchange API"]
            }
        },
        "estimationResults": {
            "projectSize": 120,
            "developmentEffort": 150,
            "effortMultiplier": 1.2,
            "developmentTime": 18
        }
    },
    {
        "projectName": "E-commerce Platform",
        "dateCreated": (datetime.now() - timedelta(days=45)).isoformat(),
        "functionPointAnalysis": {
            "externalInputs": {
                "count": 4,
                "modules": ["User registration", "Product listing", "Cart management", "Checkout"]
            },
            "externalOutputs": {
                "count": 3,
                "modules": ["Order confirmation", "Shipping update", "Invoice generation"]
            },
            "externalInquiries": {
                "count": 2,
                "modules": ["Product search", "Order tracking"]
            },
            "internalLogicalFiles": {
                "count": 3,
                "modules": ["User profiles", "Product catalog", "Order history"]
            },
            "externalInterfaceFiles": {
                "count": 2,
                "modules": ["Payment gateway", "Shipping API"]
            }
        },
        "estimationResults": {
            "projectSize": 200,
            "developmentEffort": 250,
            "effortMultiplier": 1.5,
            "developmentTime": 24
        }
    }
]