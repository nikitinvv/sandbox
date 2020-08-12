import sys
import argparse

from epics import PV


def set_pvs():
    epics_pvs = {}
    epics_pvs['Energy'] = PV('2bma:TomoScan:Energy.VAL')
    epics_pvs['Energy_Mode'] = PV('2bma:TomoScan:EnergyMode.VAL')

    epics_pvs['CloseShutterPVName']   = PV('2bma:TomoScan:CloseShutterPVName')
    epics_pvs['CloseShutterValue']    = PV('2bma:TomoScan:CloseShutterValue')
    epics_pvs['OpenShutterPVName']    = PV('2bma:TomoScan:OpenShutterPVName')
    epics_pvs['OpenShutterValue']     = PV('2bma:TomoScan:OpenShutterValue')
    # epics_pvs['ShutterStatusPVName']  = PV('2bma:TomoScan:ShutterStatusPVName')

    epics_pvs['CloseShutter']        = PV(epics_pvs['CloseShutterPVName'].get(as_string=True))
    epics_pvs['OpenShutter']         = PV(epics_pvs['OpenShutterPVName'].get(as_string=True))
    epics_pvs['ShutterStatus']         = PV('')

    return epics_pvs

def open_shutter(epics_pvs):
    """Opens the shutter to collect flat fields or projections.

    The value in the ``OpenShutterValue`` PV is written to the ``OpenShutter`` PV.
    """

    if not epics_pvs['OpenShutter'] is None:
        pv = epics_pvs['OpenShutter']
        value = epics_pvs['OpenShutterValue'].get(as_string=True)
        log.info('open shutter: %s, value: %s', pv, value)
        epics_pvs['OpenShutter'].put(value, wait=True)

def close_shutter(epics_pvs):
    """Closes the shutter to collect dark fields.

    The value in the ``CloseShutterValue`` PV is written to the ``CloseShutter`` PV.
    """
    if not epics_pvs['CloseShutter'] is None:
        pv = epics_pvs['CloseShutter']
        value = epics_pvs['CloseShutterValue'].get(as_string=True)
        log.info('close shutter: %s, value: %s', pv, value)
        epics_pvs['CloseShutter'].put(value, wait=True)


def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument("--open",action="store_true", help="Open the beamline shutter")

    args = parser.parse_args()

    epics_pvs = set_pvs()

    if args.open:
    	open_shutter(epics_pvs)
    else:
    	close_shutter(epics_pvs)


if __name__ == "__main__":
    main(sys.argv[1:])
