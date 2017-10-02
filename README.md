## docker-spawn

Docker is a containerization platform for isolating job execution environments. 

This is an experiment to attempt to automatically generate, schedule, and run docker containers for common job patterns on the Lewis and Clark College campus cluster.

This is an independent study by Benjamin Glick (@benhg, glick@lclark.edu), advised by Dr. Jens Mache (jmache@lclark.edu). Please feel free to contact me (Ben) with any questions or suggestions.


## Brief To-do list/ short project roadmap


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
- I want users to be able to interact with the cluster easily and through a GUI. Prototype I'm thinking about is the following:
- Web based form
- Takes inputs:
  - JSON specification of file structure expected (Will be a GUI to create this, more to come later)
  - Script and/or executable to run
  - CLI invocation of said script (suggestions will be available)
