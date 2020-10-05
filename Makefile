make m_pull:
	git pull upstream master

make m_push:
	git push origin master

make m_pull_fup:
	git pull origin for_upstream

make fup_pull:
	git checkout for_upstream
	git pull upstream master

make fup_push:
	git checkout for_upstream
	git push origin for_upstream