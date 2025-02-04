@echo off
start cmd /k "cd /d %~dp0\server\envs && .\domain_prediction_env\Scripts\activate && cd.. && py .\microservices\domain_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\tasks_prediction_env\Scripts\activate && cd.. && py .\microservices\task_prediction_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\file_management_env\Scripts\activate && cd.. && py .\microservices\file_management_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\report_generation_env\Scripts\activate && cd.. && py .\microservices\report_generation_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\feedback_env\Scripts\activate && cd.. && py .\microservices\feedback_service.py"
timeout /t 2
start cmd /k "cd /d %~dp0\server\envs && .\api_gateway_env\Scripts\activate && cd.. && py .\api_gateway\api_gateway.py"
timeout /t 2
start cmd /k "cd /d %~dp0\client\web_app\ && npm run dev"
timeout /t 5
start "" "http://localhost:5173/"