lab_url:
	docker logs study_lab 2>&1 | grep 'http' | tail -1