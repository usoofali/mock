import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Cropper:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.original_image = self.image.copy()
        self.image_path = image_path
        self.rect_start = None
        self.rect_end = None
        self.drawing = False
        self.crop_rect = (0, 0, self.image.shape[1], self.image.shape[0])
        self.fig, self.ax = plt.subplots()
        self.display_image()
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.key_cid = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def display_image(self):
        self.ax.clear()
        self.ax.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        x, y, w, h = self.crop_rect
        rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
        self.ax.add_patch(rect)
        plt.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        x, y = int(event.xdata), int(event.ydata)
        if self.rect_start is None:
            self.rect_start = (x, y)
            self.drawing = True
        else:
            self.rect_end = (x, y)
            self.drawing = False
            self.crop_rect = (min(self.rect_start[0], self.rect_end[0]),
                              min(self.rect_start[1], self.rect_end[1]),
                              abs(self.rect_start[0] - self.rect_end[0]),
                              abs(self.rect_start[1] - self.rect_end[1]))
            self.display_image()

    def on_key(self, event):
        if event.key == 'enter':
            if self.rect_start and self.rect_end:
                x, y, w, h = self.crop_rect
                cropped_image = self.original_image[y:y+h, x:x+w]
                cv2.imwrite(self.image_path, cropped_image)
                print(f"Cropped image saved as {self.image_path}")
            plt.close(self.fig)
        elif event.key == 'escape':
            plt.close(self.fig)
        elif event.key == 'a':  # Move rectangle left
            self.crop_rect = (self.crop_rect[0] - 10, self.crop_rect[1], self.crop_rect[2], self.crop_rect[3])
            self.display_image()
        elif event.key == 'd':  # Move rectangle right
            self.crop_rect = (self.crop_rect[0] + 10, self.crop_rect[1], self.crop_rect[2], self.crop_rect[3])
            self.display_image()
        elif event.key == 'w':  # Move rectangle up
            self.crop_rect = (self.crop_rect[0], self.crop_rect[1] - 10, self.crop_rect[2], self.crop_rect[3])
            self.display_image()
        elif event.key == 's':  # Move rectangle down
            self.crop_rect = (self.crop_rect[0], self.crop_rect[1] + 10, self.crop_rect[2], self.crop_rect[3])
            self.display_image()

image_path = "Hafsat Abubakar.jpg"
Cropper(image_path)
