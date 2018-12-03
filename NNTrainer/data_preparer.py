import scipy
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import datetime
from PIL import Image

class DataPrepare():
    def __init__(self, dataset_name, img_res=(128, 128), datanum = 100):
        self.dataset_name = dataset_name
        self.img_res = img_res
        self.datanum = datanum
        self.combine_data()

    def combine_data(self):
        folder = "./datasets/" + self.dataset_name + "/source/"
        for i in range(0, self.datanum):
            colorpath = folder + 'image_color_%04d' % i + ".png"
            depth = folder + 'image_depth_%04d' % i + ".png"
            target = folder + 'image_out_%04d' % i + ".png"
            images = map(Image.open, [colorpath, depth, target])
            new_im = Image.new('RGB', (self.img_res[0] * 3, self.img_res[1]))
            x_offset = 0
            for im in images:
                new_im.paste(im, (x_offset,0))
                x_offset += self.img_res[0]
            outpath = "./datasets/" + self.dataset_name + "/train/" + 'image_%04d' % i + ".png"
            new_im.save(outpath)

    def load_data(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "test"
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        np.random.seed(datetime.datetime.now().microsecond)
        batch_images = np.random.choice(path, size=batch_size)

        imgs_A = []
        imgs_B = []
        for img_path in batch_images:
            img = self.imread(img_path)

            h, w, _ = img.shape
            _w = int(w/2)
            img_B, img_A = img[:, :_w, :], img[:, _w:, :]

            img_A = scipy.misc.imresize(img_A, self.img_res)
            img_B = scipy.misc.imresize(img_B, self.img_res)

            # If training => do random flip
            if not is_testing and np.random.random() < 0.5:
                img_A = np.fliplr(img_A)
                img_B = np.fliplr(img_B)

            imgs_A.append(img_A)
            imgs_B.append(img_B)

        imgs_A = np.array(imgs_A)/127.5 - 1.
        imgs_B = np.array(imgs_B)/127.5 - 1.

        return imgs_A, imgs_B

    def load_batch(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "val"
        path = glob('./datasets/%s/%s/*' % (self.dataset_name, data_type))

        self.n_batches = int(len(path) / batch_size)

        for i in range(self.n_batches-1):
            batch = path[i*batch_size:(i+1)*batch_size]
            imgs_A, imgs_B = [], []
            for img in batch:
                img = self.imread(img)
                h, w, _ = img.shape
                half_w = int(w/2)
                img_B = img[:, :half_w, :]
                img_A = img[:, half_w:, :]

                img_A = scipy.misc.imresize(img_A, self.img_res)
                img_B = scipy.misc.imresize(img_B, self.img_res)

                if not is_testing and np.random.random() > 0.5:
                        img_A = np.fliplr(img_A)
                        img_B = np.fliplr(img_B)

                imgs_A.append(img_A)
                imgs_B.append(img_B)

            imgs_A = np.array(imgs_A)/127.5 - 1.
            imgs_B = np.array(imgs_B)/127.5 - 1.

            yield imgs_A, imgs_B


    def imread(self, path):
        return scipy.misc.imread(path, mode='RGB').astype(np.float)

if __name__ == '__main__':
    DataPrepare("terrain", (512,512), 301)