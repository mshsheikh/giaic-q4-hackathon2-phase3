# Phase IV Deployment Plan: Local Kubernetes Deployment

## Overview
This plan outlines the step-by-step execution process for deploying the Todo AI Chatbot application to a local Kubernetes cluster using Minikube and Helm.

## Prerequisites Checklist
- [ ] Minikube installed and functional
- [ ] Helm 3.x installed and initialized
- [ ] Docker daemon running
- [ ] kubectl installed and configured
- [ ] Docker AI (Gordon) installed
- [ ] kubectl-ai installed
- [ ] Kagent installed and configured

## Phase 1: Environment Setup

### Step 1.1: Start Minikube Cluster
**Command:**
```bash
minikube start --driver=docker --cpus=4 --memory=8192 --disk-size=20g
```

**Verification:**
```bash
kubectl cluster-info
kubectl get nodes
```

**Expected Result:** Minikube cluster running with at least one node in Ready state.

### Step 1.2: Install and Configure Helm
**Command:**
```bash
helm version
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

**Verification:**
```bash
helm list --all-namespaces
```

**Expected Result:** Helm client and server versions displayed, repositories updated successfully.

## Phase 2: Containerization

### Step 2.1: Generate Dockerfile using Docker AI (Gordon)
**Command:**
```bash
# Navigate to the project root directory
cd /mnt/e/giaic-q4-hackathon2-phase3

# Use Docker AI to generate or optimize Dockerfile
gordon create-dockerfile --language=python --framework=fastapi
```

**Alternative if Gordon is not available:**
```bash
# Create Dockerfile manually based on application requirements
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

**Verification:**
```bash
ls -la Dockerfile
cat Dockerfile
```

**Expected Result:** Dockerfile created in project root with appropriate Python/FastAPI configuration.

### Step 2.2: Build Docker Image
**Command:**
```bash
# Tag image appropriately for local deployment
docker build -t todo-ai-chatbot:latest .
```

**Verification:**
```bash
docker images | grep todo-ai-chatbot
```

**Expected Result:** Docker image built successfully with tag "todo-ai-chatbot:latest".

### Step 2.3: Tag Image for Minikube
**Command:**
```bash
# Make Docker context point to Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild image in Minikube's context
docker build -t todo-ai-chatbot:latest .

# Verify image exists in Minikube
docker images | grep todo-ai-chatbot
```

**Expected Result:** Docker image available in Minikube's Docker registry.

## Phase 3: Helm Chart Creation

### Step 3.1: Create Helm Chart Structure
**Command:**
```bash
# Create Helm chart directory
helm create todo-ai-chatbot-chart

# Remove default templates to customize
rm -rf todo-ai-chatbot-chart/templates/*
```

**Verification:**
```bash
ls -la todo-ai-chatbot-chart/
```

**Expected Result:** Helm chart directory structure created with empty templates folder.

### Step 3.2: Create Custom Helm Templates
**Command:**
```bash
# Create Deployment template
cat > todo-ai-chatbot-chart/templates/deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-ai-chatbot-chart.fullname" . }}
  labels:
    {{- include "todo-ai-chatbot-chart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-ai-chatbot-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "todo-ai-chatbot-chart.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
EOF

# Create Service template
cat > todo-ai-chatbot-chart/templates/service.yaml << 'EOF'
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-ai-chatbot-chart.fullname" . }}
  labels:
    {{- include "todo-ai-chatbot-chart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "todo-ai-chatbot-chart.selectorLabels" . | nindent 4 }}
EOF

# Create Ingress template (optional)
cat > todo-ai-chatbot-chart/templates/ingress.yaml << 'EOF'
{{- if .Values.ingress.enabled -}}
{{- $fullName := include "todo-ai-chatbot-chart.fullname" . -}}
{{- $svcPort := .Values.service.port -}}
{{- if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}
kind: Ingress
metadata:
  name: {{ $fullName }}
  labels:
    {{- include "todo-ai-chatbot-chart.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              service:
                name: {{ $fullName }}
                port:
                  number: {{ $svcPort }}
              {{- else }}
              serviceName: {{ $fullName }}
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
  {{- end }}
EOF

# Create ConfigMap template
cat > todo-ai-chatbot-chart/templates/configmap.yaml << 'EOF'
{{- if .Values.config }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-ai-chatbot-chart.fullname" . }}-config
data:
  {{- range $key, $value := .Values.config }}
  {{ $key }}: {{ $value | quote }}
  {{- end }}
{{- end }}
EOF

# Create Secret template
cat > todo-ai-chatbot-chart/templates/secret.yaml << 'EOF'
{{- if .Values.secrets }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-ai-chatbot-chart.fullname" . }}-secrets
type: Opaque
data:
  {{- range $key, $value := .Values.secrets }}
  {{ $key }}: {{ $value | b64enc | quote }}
  {{- end }}
{{- end }}
EOF
```

**Verification:**
```bash
ls -la todo-ai-chatbot-chart/templates/
```

**Expected Result:** All required template files created in the templates directory.

### Step 3.3: Configure Values File
**Command:**
```bash
# Override default values.yaml with application-specific settings
cat > todo-ai-chatbot-chart/values.yaml << 'EOF'
# Default values for todo-ai-chatbot-chart.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: todo-ai-chatbot
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "latest"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}

podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: NodePort
  port: 8000

ingress:
  enabled: false
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths: []
  tls: []

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Application-specific environment variables
env:
  ENVIRONMENT: "production"
  LOG_LEVEL: "info"

# Configuration values
config:
  app_config: |
    {
      "debug": false,
      "log_level": "info"
    }

# Secret values (these should be overridden in production)
secrets:
  api_key: "your-api-key-here"
EOF
```

**Verification:**
```bash
cat todo-ai-chatbot-chart/values.yaml
```

**Expected Result:** Custom values.yaml file created with application-specific configurations.

## Phase 4: Deployment Execution

### Step 4.1: Validate Helm Chart
**Command:**
```bash
# Validate the chart syntax and template rendering
helm lint todo-ai-chatbot-chart/

# Dry-run to see what would be deployed
helm install todo-ai-chatbot-release todo-ai-chatbot-chart/ --dry-run --debug
```

**Expected Result:** Helm chart passes validation with no errors.

### Step 4.2: Install Helm Release
**Command:**
```bash
# Install the release to the default namespace
helm install todo-ai-chatbot-release todo-ai-chatbot-chart/ --wait --timeout=10m
```

**Verification:**
```bash
# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

**Expected Result:** Deployment, pods, and services created successfully with healthy status.

### Step 4.3: Verify Application Accessibility
**Command:**
```bash
# Get service details
kubectl get svc todo-ai-chatbot-release-todo-ai-chatbot-chart

# Get Minikube IP and service port
MINIKUBE_IP=$(minikube ip)
NODE_PORT=$(kubectl get service todo-ai-chatbot-release-todo-ai-chatbot-chart -o jsonpath='{.spec.ports[0].nodePort}')

echo "Application URL: http://$MINIKUBE_IP:$NODE_PORT"
```

**Verification:**
```bash
# Test application endpoint
curl -v "http://$(minikube ip):$NODE_PORT/"
```

**Expected Result:** Successful response from the Todo AI Chatbot application.

## Phase 5: AI-Assisted Operations

### Step 5.1: Use kubectl-ai for Monitoring
**Command:**
```bash
# Use natural language to check application status
kubectl ai "show me the status of all pods in the default namespace"

# Troubleshoot any issues using AI assistance
kubectl ai "check if there are any issues with the todo-ai-chatbot deployment"
```

### Step 5.2: Optimize with Kagent
**Command:**
```bash
# Use Kagent to analyze and optimize the deployment
kagent analyze deployment todo-ai-chatbot-release-todo-ai-chatbot-chart
```

## Phase 6: Verification and Testing

### Step 6.1: Health Checks
**Command:**
```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/name=todo-ai-chatbot-chart

# Check service endpoints
kubectl get endpoints todo-ai-chatbot-release-todo-ai-chatbot-chart

# Check logs for any errors
kubectl logs -l app.kubernetes.io/name=todo-ai-chatbot-chart
```

### Step 6.2: Functional Testing
**Command:**
```bash
# Test health endpoint
curl "http://$(minikube ip):$NODE_PORT/health"

# Test readiness endpoint
curl "http://$(minikube ip):$NODE_PORT/ready"

# Test main application endpoints (adjust based on actual API)
curl "http://$(minikube ip):$NODE_PORT/docs"  # Swagger UI
```

**Expected Result:** All endpoints return successful responses.

### Step 6.3: Resource Utilization Check
**Command:**
```bash
# Check resource usage
kubectl top pods

# Check deployment status
kubectl rollout status deployment/todo-ai-chatbot-release-todo-ai-chatbot-chart
```

## Phase 7: Documentation and Handoff

### Step 7.1: Generate Deployment Documentation
**Command:**
```bash
# Create deployment summary document
cat > deployment-summary.md << EOF
# Deployment Summary - Todo AI Chatbot

## Deployment Details
- **Helm Release Name**: todo-ai-chatbot-release
- **Namespace**: default
- **Image**: todo-ai-chatbot:latest
- **Replicas**: $(kubectl get deployment todo-ai-chatbot-release-todo-ai-chatbot-chart -o jsonpath='{.spec.replicas}')
- **Service Type**: NodePort
- **External Access**: http://$(minikube ip):$(kubectl get service todo-ai-chatbot-release-todo-ai-chatbot-chart -o jsonpath='{.spec.ports[0].nodePort}')

## Status
- **Deployment Status**: $(kubectl get deployment todo-ai-chatbot-release-todo-ai-chatbot-chart -o jsonpath='{.status.conditions[?(@.type=="Available")].status}')
- **Ready Replicas**: $(kubectl get deployment todo-ai-chatbot-release-todo-ai-chatbot-chart -o jsonpath='{.status.readyReplicas}')

## Next Steps
1. Scale the deployment as needed: helm upgrade todo-ai-chatbot-release todo-ai-chatbot-chart/ --set replicaCount=3
2. Update configurations: helm upgrade todo-ai-chatbot-release todo-ai-chatbot-chart/ -f custom-values.yaml
3. Rollback if needed: helm rollback todo-ai-chatbot-release
EOF
```

### Step 7.2: Cleanup Instructions
**Command:**
```bash
# Create cleanup instructions document
cat > cleanup-instructions.md << 'EOF'
# Cleanup Instructions

## To Uninstall the Helm Release
```bash
helm uninstall todo-ai-chatbot-release
```

## To Stop Minikube
```bash
minikube stop
```

## To Delete Minikube Cluster
```bash
minikube delete
```

## To Clean Up Docker Images
```bash
# Remove the built image
docker rmi todo-ai-chatbot:latest
```
EOF
```

## Rollback Plan
1. If deployment fails during installation:
   ```bash
   helm uninstall todo-ai-chatbot-release
   ```

2. If issues arise after deployment:
   ```bash
   helm rollback todo-ai-chatbot-release
   ```

3. If configuration issues occur:
   ```bash
   helm upgrade todo-ai-chatbot-release todo-ai-chatbot-chart/ --reuse-values
   ```

## Success Criteria Verification
- [ ] Helm chart installed successfully
- [ ] Deployment is in Running state
- [ ] Service is accessible externally
- [ ] Health checks pass
- [ ] Application responds to requests
- [ ] Resource utilization is acceptable
- [ ] Documentation generated

## Post-Deployment Steps
1. Monitor application performance for 15 minutes
2. Verify all acceptance criteria from the spec are met
3. Document any deviations or issues encountered
4. Prepare scaling recommendations based on observed resource usage