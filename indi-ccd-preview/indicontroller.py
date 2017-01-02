from indicamera import INDICamera
from indiclient import INDIClient
from astropy.io import fits
from datetime import datetime
import os
import scipy.misc
import numpy
import matplotlib.pyplot as plt
from glob import glob
import pprint

class INDIImage:
    def __init__(self, workdir, fits_file, extension = 'jpg', log_y = True, bins = 256):
        self.fits_file = fits.open('/'.join([workdir, fits_file]))
        self.id = datetime.utcnow().isoformat()
        self.workdir = workdir
        self.extension = extension
        scipy.misc.imsave(self.__path('image'), self.fits_file[0].data)
        self.__make_histogram(self.fits_file[0].data, log_y, bins)

    def imagefile(self):
        return self.__filename('image')

    def histogram(self):
        return self.__filename('histogram')

    def __filename(self, name):
        return '{0}-{1}.{2}'.format(name, self.id, self.extension)

    def __path(self, name):
        return '{0}/{1}'.format(self.workdir, self.__filename(name))

    def __make_histogram(self, data, log_y, bins):
        plt.clf()
        plt.hist(data.flatten() , bins=256)
        plt.xlim([0, 255])
        if log_y:
            plt.yscale('log')
        plt.savefig(self.__path('histogram'))


class INDIController:
    def __init__(self, workdir):
        self.client = INDIClient()

        self.workdir = workdir
        if not os.path.isdir(self.workdir):
            os.makedirs(self.workdir)


    def devices(self):
        properties = self.client.get_properties()
        devices = list(set([property['device'] for property in properties]))
        devices.sort()
        return devices

    def properties(self, device):
       return self.client.get_properties(device) 

    def property(self, device, property):
        property_element = property.split('.')
        return self.client.get_properties(device, property_element[0], property_element[1])[0]

    def set_property(self, device, property, value):
        property_element = property.split('.')
        self.client.set_property_sync(device, property_element[0], property_element[1], value)
        return self.property(device, property)

    def preview(self, device, exposure):
        imager = INDICamera(device, self.client)
        if not imager.is_camera():
            raise RuntimeError('Device {0} is not an INDI CCD Camera'.format(device))
        imager.set_output(self.workdir, 'IMAGE_PREVIEW')
        imager.shoot(exposure)
        return INDIImage(self.workdir, 'IMAGE_PREVIEW.fits')


