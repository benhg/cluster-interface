Brief To-do list/ short project roadmap
(Things that are struck through are done, not removed)

**FRONT END/USER INTERACTION**
- Python API/interface
- CL tools
- ~~Web-based GUI~~
- to interact with:

**BACK END**
- Submit, status, cancel of tasks
- Interact with scheduler
- Ideally, the following process occurs for each submit
  - User submits job
  - Job is containerized
  - ~~Inputs are staged~~
  - Job is submitted to cluster scheduler
  - Job executes/fails
  - User is notified
  - Outputs are staged and made available
- ~~Database to track metadata on jobs~~
 
**USER INPUTS**
- I want users to be able to interact with the cluster easily and through a GUI. Prototype I'm thinking about is the following:
- ~~Web based form~~
- Takes inputs:
  - JSON specification of file structure expected (Will be a GUI to create this, more to come later)
  - Handle libraries/modules/apps/dependencies
  - Script and/or executable to run
  - CLI invocation of said script (suggestions will be available)
  
**Things To Write**
- ~~Flask app to handle web backend~~
- ~~Web frontend~~
- System interaction layer
  - File Structure
  - ~~Security~~ (V. 1 is working. Moving away from security for a little while.)
    -Oauth (maybe globus auth is a good place to start?)
    - Possibly a place to test stewarship model?
      - Requiring a manual override for some types of jobs
      - Small sandboxed jobs can be run without stewardship
      - Larger/size unlimited jobs must be manually approved by an admin
      - This keeps people without permission from using large amounts of compute time
      - Register and change login page
  - Execution
- Data Staging Layer
  - Parsing descriptions of filesystems
  - and generating them
  - Staging input data
    - From head node
    - From Internet
    - Over Globus (?)
  - Containerization layer
  - Execution Layer
  
 
