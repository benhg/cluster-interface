Brief To-do list/ short project roadmap


**FRONT END/USER INTERACTION**
- Python API/interface
- CL tools
- Web-based GUI
- to interact with:

**BACK END**
- Submit, status, cancel of tasks
- Interact with scheduler
- Ideally, the following process occurs for each submit
  - User submits job
  - Job is containerized
  - Inputs are staged
  - Job is submitted to cluster scheduler
  - Job executes/fails
  - User is notified
  - Outputs are staged and made available
- Database to track metadata on jobs
 
**USER INPUTS**
I want users to be able to interact with the cluster easily and through a GUI. Prototype I'm thinking about is the following:
- Web based form
- Takes inputs:
  - JSON specification of file structure expected (Will be a GUI to create this, more to come later)
  - Script and/or executable to run
  - CLI invocation of said script (suggestions will be available)
  
 
