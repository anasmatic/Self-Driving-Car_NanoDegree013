#**Finding Lane Lines on the Road** 

##Self-Driving Car NanoDegree

###1st Project, Term1

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


---

### Reflection

###1. Pipeline Description:
A video is a stack of frames, and every frame is an images, so we can apply this process on every frame.
My pipeline consisted of 5 steps using [opencv](http://opencv.org/documentation.html) : 
 - Convert incoming image to **gray scale** , handling one channel of color is better than working with 3 channels -R G B-
[Grayscale]: (/_README_IMAGES/gray.png "Grayscale")
 - **Blur** the gray image, this will reduce any noise in the picture that may lead to fake edges.
['image2']: /_README_IMAGES/blur.png "GaussianBlur"
 - Convert the Blur image to edges, using **canny edges** detector, now we have a lot of lines in the photo.
[image3]: ./_README_IMAGES/edges.png "Canny"
 - Mask the image to keep only the **region of interest**, most probably lanes will form a triangle -*Trapezoid actually*- in the lower half of the image, so we need to focus only on that shape.
[image4]: ./_README_IMAGES/masked.png "region of interest"
 - Find dominant lines in image using **Hough Line Transform** , and draw them using draw_lines() function .
[image5]: ./_README_IMAGES/lines.png "dominant lines"
 - Finally merge the dominant lines with the original- colored- image
[image6]: ./_README_IMAGES/final.png "Final image"
**More about draw_lines() function** :
 - As suggested , slop sign ( *+ or -* ) can be a good indicator of line relation to lane, so lines with slopes negative are related to left lane, and vice versa.
 - Dividing the image in two vertical halves, would help decreasing lines madness ! , so if you are a line with negative slop, you have to be on the left side of the image, or else I'll ignore you ..
 - Looping over lines, I would find the farthest and the nearest points, then imagine a line between them, **this is my dominant line** .
 - I save the slop (**m**) and the intersect (**b**) of this line, and use it to draw a line from the top of the **region of interest** to the button of the image. (**y = top or bottom of image , x = y-b /m**)

![alt text][image7]


###2. Identify potential shortcomings with your current pipeline

the first Shortcoming of this pipe line is when we have lighter Asphalt color or shining light leading to messy edges.

Another shortcoming is when I have high value for the horizon, that will force me to detect very small lines, they are not small but far and looks small, and detecting such small lines may lead to crazy lines crossing the picture ! trying to detect some white point in the middle of the image assuming it is a lane line !
![image of crazy lines][image8]

this could be a shortcoming also : car won't be able to recognize connected lane from dotted lane using the (dominant line technique), and therefore it can change lanes while traffic laws may won't allow changing lanes at interactions.
![image of connected lanes][image9]

and finally if we got a car ahead this pipeline will fail.

###3. Suggest possible improvements to your pipeline

keep the horizon low ! , this will help process curved lanes, and eliminate small lines problem when we use a high threshold. 

Smoothing algorithm to stop the line from jumping would make it looks better.
