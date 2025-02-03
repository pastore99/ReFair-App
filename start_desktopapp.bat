@echo off
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\microservices\file_management_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\microservices\domain_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\microservices\task_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\microservices\feedback_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\api_gateway\api_gateway.py"
timeout /t 2
start cmd /k "cd /d %~dp0\refair-server && .\env\Scripts\activate && cd.. && py .\desktop_app\index.py"