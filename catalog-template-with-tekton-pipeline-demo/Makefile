# Install minikube and kubectl with homebrew (MacOS Only)
install:
	brew install minikube
	brew install kubectl

install-resources:
	kubectl apply --filename https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml
	kubectl apply --filename \
	https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
	kubectl apply --filename \
	https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml
	kubectl apply --filename \
	https://storage.googleapis.com/tekton-releases/dashboard/latest/release-full.yaml

	kubectl apply -f https://raw.githubusercontent.com/tektoncd/catalog/v1beta1/wget/wget.yaml

install-defined-resources:
	kubectl apply -f tasks/create-repo.yaml -f tasks/clone-repo.yaml -f tasks/upload-catalog-json.yaml
	kubectl apply -f pipelines/repo-setup.yaml -f pipelines/update-downstream.yaml
	kubectl apply -f service_accounts/rbac.yaml
	kubectl apply -f eventlisteners/eventlistener.yaml
	kubectl apply -f trigger-bindings/github-push-trigger-binding.yaml
	kubectl apply -f trigger-templates/github-push-trigger-template.yaml
	kubectl apply -f secrets/webhook-secret.yaml
	kubectl apply -f secrets/token-secret.yaml
run:
	kubectl delete pipelinerun run-pipeline
	kubectl apply -f runners/pipeline-runner.yaml

# Forward the port to access the Tekton dashboard at http://localhost:9097
dashboard:
	kubectl port-forward -n tekton-pipelines service/tekton-dashboard 9097:9097

forward-port:
	kubectl port-forward service/el-github-push 8080

tunnel:
	ngrok http http://localhost:8080