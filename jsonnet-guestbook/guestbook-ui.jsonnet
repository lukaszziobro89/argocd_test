local params = import 'params.libsonnet';

[
   {
      "apiVersion": "v1",
      "kind": "Service",
      "metadata": {
         "name": params.name
      },
      "spec": {
         "ports": [
            {
               "port": params.servicePort,
               "targetPort": params.containerPort
            }
         ],
         "selector": {
            "app": params.name
         },
         "type": params.type
      }
   },
{
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "name": "before",
    "annotations": {
      "argocd.argoproj.io/hook": "PreSync",
      "argocd.argoproj.io/hook-delete-policy": "BeforeHookCreation"
    }
  },
  "spec": {
    "template": {
      "spec": {
        "containers": [
          {
            "name": "sleep",
            "image": "alpine:latest",
            "command": [
              "echo",
              "FROM PreSync ArgoCD Hook"
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    },
    "backoffLimit": 0
  }
},
{
  "apiVersion": "batch/v1",
  "kind": "Job",
  "metadata": {
    "name": "after",
    "annotations": {
      "argocd.argoproj.io/hook": "PostSync",
      "argocd.argoproj.io/hook-delete-policy": "BeforeHookCreation"
    }
  },
  "spec": {
    "template": {
      "spec": {
        "containers": [
          {
            "name": "sleep",
            "image": "alpine:latest",
            "command": [
              "echo",
              "FROM PreSync ArgoCD Hook"
            ]
          }
        ],
        "restartPolicy": "Never"
      }
    },
    "backoffLimit": 0
  }
},
   {
      "apiVersion": "apps/v1",
      "kind": "Deployment",
      "metadata": {
         "name": params.name
      },
      "spec": {
         "replicas": params.replicas,
         "revisionHistoryLimit": 3,
         "selector": {
            "matchLabels": {
               "app": params.name
            },
         },
         "template": {
            "metadata": {
               "labels": {
                  "app": params.name
               }
            },
            "spec": {
               "containers": [
                  {
                     "image": params.image,
                     "name": params.name,
                     "ports": [
                     {
                        "containerPort": params.containerPort
                     }
                     ]
                  }
               ]
            }
         }
      }
   }
]
