=======================================================
         Network Analytics Server CI Scripts
=======================================================

-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
GENERAL OVERVIEW
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------


Network Analytics Server Requires two VMs:
   i) A Controller VM (Windows 7)
   ii) The SUT VM (Windows Server 2012)


                           -------    --------
   Jenkins (optional) <--- |     |--->|      |
                           |     |    |      |
                           -------    --------
                          Controller     SUT

This CI repo provides several scripts which execute the Continious Intergretation
of the Network Analytics Server. The execution and description of these scripts are 
detailed below.


-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
   CONTROLLER VM SYSTEM REQUIREMENTS
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
Requires Windows 7
Requires Maven & Java jdk (1.7)
Requires Mozilla firefox (version)
Requires GIT
Requires Powershell v4 installed
Requires Powershell CLI installed (Currently installed - VMware vSphere PowerCLI 6.0 Release 1 build 2548067)
   
   PowerCLI Version
   ----------------
   VMware vSphere PowerCLI 6.0 Release 1 build 2548067
   ---------------
   Component Versions
   ---------------
   VMWare AutoDeploy PowerCLI Component 6.0 build 2358282
   VMWare ImageBuilder PowerCLI Component 6.0 build 2358282
   VMware License PowerCLI Component 6.0 build 2315846
   VMware vSphere PowerCLI Component 6.0 build 2548068
   VMware Cloud Infrastructure Suite PowerCLI Component 6.0 build 2548068
   VMware HA PowerCLI Component 6.0 build 2510422
   VMware PowerCLI Component for Storage Management 6.0 build 2522368
   VMware VDS PowerCLI Component 6.0 build 2548068



-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
   CONTROLLER SET UP & CONFIGURATION
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------

   Create Store Key for PowerShell CLI
   -----------------------------------
   The controller uses PowerCli. PowerCli is a powershell set of snapins that
   allow the remote administration of VShpere VMs. The Network Analytics Server uses a credential file for the 
   user vSPhere user 'NetAnServerCI'.

   To configure the user and password for vm administration the user has two options:
      i) Setup the user 'NetAnServerCI' as a user who can roll back a VM, i.e. get the target VM (SUT) added the the NetAnServerCI profile in vSphere
      ii) Create a new credentials xml file for a new user, who already exists in vSphere, and has privaleges to take and restore a VM to snapshots. 

   To create a new credentials.xml file, run these from PowerCli Shell 
   New-VICredentialStoreItem -Host <virtual centre name> -User <username> -Password <password> -File <path to your credentials file>.xml
   The newly created key file should be stored in the credential_store directory
   A KEY IS UNIQUE TO EACH MACHINE - IT MUST BE CREATED FOR THE SAME USER ON EVERY MACHINE THIS SCRIPT WILL RUN ON.
   PowerCLI is required run these commands.


   SFTP Module for Uploading results
   ---------------------------------
   This is required to SFTP results to the CI Radiator page.
   SFTP PowerShell Snap-In
   Beta Release [V2.0b]
   http://www.k-tools.nl/index.php/download-sftp-powershell-snap-in/
   Need this to be installed for sftp.
   Need to add public key of user from controller to Radiator Server authorized keys.
   $key in module Upload_Results is path for private key of the user.

   Remoting Setup and Configuration
   --------------------------------
   This is required for the remote execution of powershell scripts
   Please refer to comments in JIRA http://jira-oss.lmera.ericsson.se/browse/EQEV-21379 for set-up

   Clone Repo
   --------------------------------
   This repo must be cloned to the Desktop of the Controller VM (Windows 7)

      git clone ssh://<signum>@gerrit.ericsson.se:29418/OSS/com.ericsson.eniq/network-analytics-server-ci

   Update CI-Config.xml
   --------------------------------
   Once the CI repo is cloned, to execute the CI scripts, the ./config/ci-config.xml must be updated to
   point to the required VM and required snapshots.
   The name attribute of <virtual-host> is required. This is the SUT host name
   The <prereq-snapshot> is the snapshot that contains the full Network Analytics Server prerequisites installed
   The <fullinstall-snapshot> is the snapshot that contains a fully installed version of the platform
   The <upgrade-snapshot> is a snapshot that is a full install snapshot, this should be at least N-1 versions behind upgrade, and on the supported upgrade path.

   Sample CI-Config.xml

   <?xml version="1.0"?>
   <config>
      <virtual-host name="atclvm2054">
         <prereq-snapshot>Windows2012_PsRemotingV4</prereq-snapshot>
         <fullinstall-snapshot>R3A26_Full_Manual_Install</fullinstall-snapshot>
         <upgrade-snapshot>R3A26_Full_Manual_Install</upgrade-snapshot>
      </virtual-host>
   </config> 

-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
   EXECUTING NETWORK ANALYTICS SERVER CI
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------

There are three sets of tests to run when executing Network Analytics Server CI:

   i)   The Network Analytics Server Platform
   ii)  Adhoc Enabler
   iii) The Feature Installer 


   Executing the Network Analytics Server Plaform CI
   --------------------------------------------------

      Overview: 
      The Network Analytics Server platform CI restores the VM to a snapshot that has all of the platform prerequisites installed for the platform.
      (Please refer to the Network Analytics Server Installation Instruction for details). It then downloads the latest version of the Network Analytics Server
      Media from Nexus, installs the media, executes TAF test cases, executes the python exe post install sanity testcases, generates a test report,
      zips the results and sftps to the CI radiator page. (These results are then handled by the CI team and presented on the CI radiator).

      Script Execution:
      To execute the Platform CI test cases execute the following script in a Powershell shell opened as administrator on the Controller VM.

         ./start_install_and_regression.ps1 

      NOTE: the script assumes that all vms are controlled by atvcen1.athtem.eei.ericsson.se and in the athtem.eei.ericsson.se domain. 



   Executing the Network Analytics Server Adhoc Enabler CI
   -------------------------------------------------------
      Overview: 
      The Network Analytics Server Adhoc Enabler CI restores the VM to a snapshot that has a full installation of the Network Analytics Server.
      It is required to update this snapshot when significant changes have been made to the platform. It should be carried out frequently.
      (Please refer to the Network Analytics Server Installation Instruction for details). It then downloads the latest version of the Network Analytics Server
      Ad hoc Media from Nexus, installs the media, executes the python exe post install sanity testcases, generates a test report,
      zips the results and sftps to the CI radiator page. When executing this script it will execute all of the Platform test cases also.

      Script Execution:
      To execute the Ad-Hoc CI test cases execute the following script in a Powershell shell opened as administrator on the Controller VM.

         ./start_install_and_regression.ps1 -TEST_AD_HOC

      NOTE: the script assumes that all vms are controlled by atvcen1.athtem.eei.ericsson.se and in the athtem.eei.ericsson.se domain. 


   Executing the Network Analytics Server Feature Installer CI
   -----------------------------------------------------------
      Overview: 
      The Network Analytics Server Feature Installer CI restores the VM to a snapshot that has a full installation of the Network Analytics Server.
      It is required to update this snapshot when significant changes have been made to the platform. It should be carried out frequently.
      (Please refer to the Network Analytics Server Installation Instruction for details). 

      The fully installed Network Analytics Server platform snapshot MUST BE UPDATED WITH THE LATEST MODULES FOR CI TO TEST WHAT HAS BEEN DELIVERED.
      These updated modules are transferred as part of the CI run. It is NOT performed as an upgrade.
      It transfers two sample feature packages to the SUT, version-one.zip and version-two.zip. These are then installed, where version-two is an upgrade.
      TAF is then executed (note that TAF carries out the upgrade i.e. installation of version-two.zip) and then executes the python exe testcases, 
      zips the results and attempts to transfer to CI radiator page

      Script Execution:
      To execute the Ad-Hoc CI test cases execute the following script in a Powershell shell opened as administrator on the Controller VM.

         ./start_install_and_regression_feature_installer.ps1 

      NOTE: the script assumes that all vms are controlled by atvcen1.athtem.eei.ericsson.se and in the athtem.eei.ericsson.se domain. 


-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------
   FUNCTION DETAILS / EXPLANATIONS
-----------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------

VMRollback:Reset-VM function parameters in: start_install_and_regression.ps1
----------------------------------------------------------------------------
$CREDENTIALS_XML [string] the absolute path to xml credentials for vSphere User for atvcen1. See above
$VIRTUAL_CENTER [string] the fully qualified domain name of the virtual centre (e.g. atvcen1.athem.eei.ericsson.se)
$targetVm [string] name of the vm (e.g. atclvm2054).
$snapShot [string] name of the snapshot to rollback to.


PostInstallExeRunner:Start-PostInstallExe function parameters in: start_install_and_regression.ps1
--------------------------------------------------------------------------------------------------
$REMOTE_SERVER [string] the targetted remote VM - fully qualified name e.g. atclvm2054.athtem.eei.ericsson.se
$LOG_DIRECTORY [string] the absolute path on the SUT to the log files to test
$INSTALL_LOCATION [string] the absolute path to where to deploy the package e.g. "C:\"
$RESULTS_DIR [string] the destination Locally (absolute path) where the html results will be transferred back to
$BUILD_VERSION [string] the current build version (will append to results file)
