import time
from epics import PV

def set_pvs():
    epics_pvs = {}

    camera_prefix = '2bmbSP1:cam1:'
    epics_pvs['CamAcquire']           = PV(camera_prefix + 'Acquire')
    epics_pvs['CamTriggerMode']       = PV(camera_prefix + 'TriggerMode')
    epics_pvs['CamNumImages']         = PV(camera_prefix + 'NumImages')
    epics_pvs['CamImageMode']         = PV(camera_prefix + 'ImageMode')

    epics_pvs['CamExposureMode']     = PV(camera_prefix + 'ExposureMode')
    epics_pvs['CamTriggerOverlap']   = PV(camera_prefix + 'TriggerOverlap')
    epics_pvs['CamArrayCallbacks']   = PV(camera_prefix + 'ArrayCallbacks')
    epics_pvs['CamFrameRateEnable']  = PV(camera_prefix + 'FrameRateEnable')
    epics_pvs['CamTriggerSource']    = PV(camera_prefix + 'TriggerSource')

    return epics_pvs

def wait_pv(epics_pv, wait_val, timeout=-1):
    """Wait on a pv to be a value until max_timeout (default forever)
       delay for pv to change
    """

    time.sleep(.01)
    start_time = time.time()
    while True:
        pv_val = epics_pv.get()
        if isinstance(pv_val, float):
            if abs(pv_val - wait_val) < EPSILON:
                return True
        if pv_val != wait_val:
            if timeout > -1:
                current_time = time.time()
                diff_time = current_time - start_time
                if diff_time >= timeout:
                    print('  *** ERROR: DROPPED IMAGES ***')                  
                    return False
            time.sleep(.01)
        else:
            return True

def set_trigger_mode(epics_pvs, trigger_mode):
    """Sets the trigger mode SIS3820 and the camera.

    Parameters
    ----------
    trigger_mode : str
        Choices are: "FreeRun" or "PSOExternal"

    num_images : int
        Number of images to collect.  Ignored if trigger_mode="FreeRun".
        This is used to set the ``NumImages`` PV of the camera.
    """

    epics_pvs['CamAcquire'].put('Done') ###
    wait_pv(epics_pvs['CamAcquire'], 0) ###
    print('set trigger mode: ', trigger_mode)
    if trigger_mode == 'FreeRun':
        epics_pvs['CamImageMode'].put('Continuous', wait=True)
        epics_pvs['CamTriggerMode'].put('Off', wait=True)
        wait_pv(epics_pvs['CamTriggerMode'], 0)
    else: # set camera to external triggering
        # These are just in case the scan aborted with the camera in another state
        epics_pvs['CamTriggerMode'].put('Off', wait=True)
        epics_pvs['CamTriggerSource'].put('Line2', wait=True)
        epics_pvs['CamTriggerOverlap'].put('ReadOut', wait=True)
        epics_pvs['CamExposureMode'].put('Timed', wait=True)

        epics_pvs['CamImageMode'].put('Multiple')
        epics_pvs['CamArrayCallbacks'].put('Enable')
        epics_pvs['CamFrameRateEnable'].put(0)

        epics_pvs['CamNumImages'].put(100, wait=True)
        epics_pvs['CamTriggerMode'].put('On', wait=True)
        wait_pv(epics_pvs['CamTriggerMode'], 1)

def main():
    epics_pvs = set_pvs()
    count = 1
    while (True):
        print(count)
        count += 1
        set_trigger_mode(epics_pvs, 'PSOExternal')
        epics_pvs['CamAcquire'].put('Acquire')
        wait_pv(epics_pvs['CamAcquire'], 1)        
        set_trigger_mode(epics_pvs, 'FreeRun')
        epics_pvs['CamAcquire'].put('Acquire')
        wait_pv(epics_pvs['CamAcquire'], 1)

if __name__ == "__main__":
    main()
