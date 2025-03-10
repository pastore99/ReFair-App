@echo off
start cmd /k "cd /d %~dp0\server\envs && .\domain_prediction_env\Scripts\activate && cd.. && python .\microservices\domain_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\tasks_prediction_env\Scripts\activate && cd.. && python .\microservices\task_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\file_management_env\Scripts\activate && cd.. && python .\microservices\file_management_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\report_generation_env\Scripts\activate && cd.. && python .\microservices\report_generation_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\feedback_env\Scripts\activate && cd.. && python .\microservices\feedback_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\api_gateway_env\Scripts\activate && cd.. && python .\api_gateway\api_gateway.py"
timeout /t 2
start cmd /k "cd /d %~dp0\client\desktop_app\ && .\desktop_app_env\Scripts\activate && cd.. && python .\desktop_app\index.py"