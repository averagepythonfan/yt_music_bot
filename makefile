lab_url:
	docker logs study_lab 2>&1 | grep 'http' | tail -1


deploy_dev:
	poetry run ansible-playbook playbooks/dev.yml --tags="up"


deploy_prod:
	poetry run ansible-playbook playbooks/prod.yml --tags="up"


down_dev:
	poetry run ansible-playbook playbooks/dev.yml --tags="down"


down_prod:
	poetry run ansible-playbook playbooks/prod.yml --tags="down"
