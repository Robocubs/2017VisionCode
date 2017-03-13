import java.util.ArrayList;
import java.util.List;
import edu.wpi.first.wpilibj.networktables.*;
import edu.wpi.first.wpilibj.tables.*;
import edu.wpi.cscore.*;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfInt;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Rect;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;
public class Main {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}
	private static Mat blurOutput = new Mat();
	private static Mat rgbThresholdOutput = new Mat();
	private static ArrayList<MatOfPoint> findContoursOutput = new ArrayList<MatOfPoint>();
	private static ArrayList<MatOfPoint> convexHullsOutput = new ArrayList<MatOfPoint>();
	private static ArrayList<MatOfPoint> filterContoursOutput = new ArrayList<MatOfPoint>();
	private static NetworkTable vision;
	public static void main(String[] args) {
		/**
		 * Load the OpenCV native library.
		 */
		System.loadLibrary("opencv_java310");
		/**
		 * Connect to NetworkTables, set our team and initialize the connection.
		 * @duplicate
		 */
		//NetworkTable.setClientMode();
		//NetworkTable.setTeam(1701);
		//NetworkTable.initialize();
		/**
		 * Set the port to stream the recieved image on. According to FRC 2017 regulations, this must be between 1180 and 1190!
		 */
		int streamPort = 1188;
		/**
		 * Make a MotionJPEG server to stream the input.
		 */
		MjpegServer inputStream = new MjpegServer("MJPEG Server", streamPort);
		/**
		 * Configure our USB camera.
		 */
		UsbCamera camera = setUsbCamera(2, inputStream);
		camera.setResolution(640, 480);
		/**
		 * Create a CvSink to grab images and send them to OpenCV.
		 */
		CvSink imageSink = new CvSink("CV Image Grabber");
		imageSink.setSource(camera);
		/**
		 * Create a CvSource to use the CvSink from.
		 */
		CvSource imageSource = new CvSource("CV Image Source", VideoMode.PixelFormat.kMJPEG, 640, 480, 10);
		MjpegServer cvStream = new MjpegServer("CV Image Stream", streamPort + 1);
		cvStream.setSource(imageSource);
		/**
		 * All Mats and Lists should be stored outside of the loop to avoid
		 * performance issues.
		 */
		Mat inputImage = new Mat();
		Mat hsv = new Mat();
		/**
		 * Now, infinitely process the image!
		 */
		while(true) {
			/**
			 * Grab a frame. If it has a frame time of zero,
			 * there was an error. Then we skip it and continue.
			 */
			long frameTime = imageSink.grabFrame(inputImage);
			if(frameTime == 0) {
				continue;
			}
			/**
			 * Below is where you would do your OpenCV operations on the
			 * provided image. We use the process function, which we
			 * define after the main function in our version.
			 */
			process(hsv);
			/**
			 * Finally, write the processed frame to the CvSink.
			 */
			imageSource.putFrame(hsv);
		}
	}
	/**
	 * Set the USB camera to grab the image from.
	 * @param  cameraId Which camera to grab the image from.
	 * @param  server   The MJPEG server to apply the image to.
	 */
	private static UsbCamera setUsbCamera(int cameraId, MjpegServer server) {
		UsbCamera camera = new UsbCamera("CoprocessorCamera", cameraId);
		server.setSource(camera);
		return camera;
	}
	/**
	 * This is the primary method that runs the entire pipeline and
	 * updates the output.
	 * @param  source A Mat object.
	 * @example process(hsv);
	 */
	public static void process(Mat source) {
		System.out.println("Starting processing...");
		/**
		 * Attempt to set NetworkTables up.
		 */
		try {
			NetworkTable.setClientMode();
			NetworkTable.setTeam(1701);
			NetworkTable.setIPAddress("10.17.1.37");
			NetworkTable.initialize();
			vision = NetworkTable.getTable("vision");
		} catch (Exception e) {
			e.printStackTrace();
		}
		/**
		 * @begin AutogenGRIP
		 */
		/**
		 * @step Blur
		 */
		Mat blurInput = source;
		BlurType blurType = BlurType.get("Gaussian Blur");
		double blurRadius = 1.8018018018018018;
		blur(blurInput, blurType, blurRadius, blurOutput);
		/**
		 * @step RGB_Threshold
		 */
		Mat rgbThresholdInput = blurOutput;
		double[] rgbThresholdRed = { 121.08812949640286, 197.0454545454545 };
		double[] rgbThresholdGreen = { 215.18884892086334, 255.0 };
		double[] rgbThresholdBlue = { 198.48920863309354, 255.0 };
		rgbThreshold(rgbThresholdInput, rgbThresholdRed, rgbThresholdGreen, rgbThresholdBlue, rgbThresholdOutput);
		/**
		 * @step Convex_Hulls
		 */
		ArrayList<MatOfPoint> convexHullsContours = findContoursOutput;
		convexHulls(convexHullsContours, convexHullsOutput);
		/**
		 * @step Filter_Contours
		 */
		ArrayList<MatOfPoint> filterContoursContours = convexHullsOutput;
		double filterContoursMinArea = 20.0;
		double filterContoursMinPerimeter = 0.0;
		double filterContoursMinWidth = 0.0;
		double filterContoursMaxWidth = 150.0;
		double filterContoursMinHeight = 0.0;
		double filterContoursMaxHeight = 220.0;
		double[] filterContoursSolidity = { 100.0, 100.0 };
		double filterContoursMaxVertices = 25.0;
		double filterContoursMinVertices = 4.0;
		double filterContoursMinRatio = 0.0;
		double filterContoursMaxRatio = 100.0;
		filterContours(filterContoursContours, filterContoursMinArea, filterContoursMinPerimeter, filterContoursMinWidth, filterContoursMaxWidth, filterContoursMinHeight, filterContoursMaxHeight, filterContoursSolidity, filterContoursMaxVertices, filterContoursMinVertices, filterContoursMinRatio, filterContoursMaxRatio, filterContoursOutput);
		/**
		 * @end AutogenGRIP
		 */
		List<MatOfPoint> possibleRect = new ArrayList<MatOfPoint>();
		List<MatOfPoint> possibleGoal = new ArrayList<MatOfPoint>();
		System.out.println(String.format("filterContoursOutput size: %s", filterContoursOutput.size()));
		processContours(filterContoursOutput, possibleRect, possibleGoal);
		/** 
		 * Processing for rectangles.
		 */
		double toleranceDW = 2.3;
		double toleranceHW = .5;
		double toleranceWW = .2;
		double score = 0;
		double rightRectSide = -1;
		double toleranceM = 10;
		double newPercentError = 0;
		boolean gearTargetLinedUp = false;
		boolean passesHWTest = false;
		boolean gearTargetFound = false;
		int resolutionX = 640;
		System.out.println("Starting gear vision...");
		System.out.println(String.format("possibleRect size: %s", possibleRect.size()));
		if(possibleRect.size() > 1) {
			for(int i = 0; i < possibleRect.size() - 1; i++) {
				Rect rect1 = Imgproc.boundingRect(possibleRect.get(i));
				System.out.println("Creating boundingRect rect1...");
				for(int j = i + 1; j < possibleRect.size(); j++) {
					Rect rect2 = Imgproc.boundingRect(possibleRect.get(j));
					System.out.println("Creating boundingRect rect2...");
					if(rect1.width >= (1 - (.5 * toleranceWW)) * rect2.width && rect1.width <= (1 + (.5 * toleranceWW)) * rect2.width) {
						System.out.println("The two rects pass the W:W test.");
						double distance;
						double width = (rect1.width + rect2.width) / 2;
						if(rect1.x <= rect2.x) {
							distance = rect2.x - (rect1.x + rect1.width);
							System.out.println("Rect1 is to the left.");
						} else {
							distance = rect1.x - (rect2.x + rect2.width);
							System.out.println("Rect2 is to the left.");
						}
						if(distance >= width * (3.125 - (.5 * toleranceDW)) && distance <= width * (3.125 + (.5 * toleranceDW))) {
							System.out.println("The two rect pass the D:W test.");
							double rect1Score = Math.abs(((rect1.height / rect1.width) - 2.5) / 2.5) * 100;
							double rect2Score = Math.abs(((rect2.height / rect2.width) - 2.5) / 2.5) * 100;
							double separationScore = Math.abs(((distance / width) - 3.125) / 3.125) * 100;
							double widthScore = Math.abs(((rect1.width / rect2.width) - 1) / 1) * 100;
							double newScore = 100 - .25 * (rect1Score + rect2Score + separationScore + widthScore);
							if(newScore > score && newScore >= 50) {
								gearTargetFound = true;
								score = newScore;
								if(rect1.x > rect2.x) {
									rightRectSide = rect1.x + rect1.width;
									if(rect1.height <= (2.5 + (.5 * toleranceHW)) * rect1.width && rect1.height >= (2.5 - (.5 * toleranceHW)) * rect1.width) {
										System.out.println("The rect passes the H:W ratio test.");
										passesHWTest = true;
										newPercentError = Math.abs(((rect1.height / rect1.width) - 2.5) / 2.5) * 100;
									}
								} else {
									rightRectSide = rect2.x + rect2.width;
									if (rect2.height <= (2.5 + (.5 * toleranceHW)) * rect2.width && rect2.height >= (2.5 - (.5 * toleranceHW)) * rect2.width) {
										System.out.println("The rect passes the H:W ratio test.");
										passesHWTest = true;
										newPercentError = Math.abs(((rect2.height / rect2.width) - 2.5) / 2.5) * 100;
									}
								}
								System.out.println("=== These two rects are better than the last! ===");
								System.out.println("The two rects are lower in score than the previous ones, or the two rects were too low in score.");
							} else {
								System.out.println("The two rects fail the D:W test.");
							}
						} else {
							System.out.println("The two rects fail the W:W test.");
						}
					}
				}
			}
		} else if(possibleRect.size() == 1) {
			Rect rect = Imgproc.boundingRect(possibleRect.get(0));
			rightRectSide = rect.x + rect.width;
			if(rect.height <= (2.5 + (.5 * toleranceHW)) * rect.width && rect.height >= (2.5 - (.5 * toleranceHW)) * rect.width) {
				System.out.println("The rect passes the H:W ratio test.");
			}
			newPercentError = Math.abs(((rect.height / rect.width) - 2.5) / 2.5) * 100;
			gearTargetFound = true;
		}
		if(gearTargetFound) {
			if(rightRectSide >= (.5 * resolutionX) - (.5 * toleranceM) && rightRectSide <= (.5 * resolutionX) + (.5 * toleranceM)) {
				gearTargetLinedUp = true;
			}
		}
		try {
			vision.putBoolean("gearTargetFound", gearTargetFound);
			vision.putNumber("gearTargetX", rightRectSide);
			vision.putBoolean("gearPassesHWTest", passesHWTest);
			vision.putNumber("gearTargetHWError", newPercentError);
			vision.putBoolean("gearTargetLinedUp", gearTargetLinedUp);
			/**
				vision.putBoolean("goalTargetFound", true);
				vision.putNumber("goalTargetX", 50);
				vision.putNumber("goalTargetY", 50);
			 */
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	public static void processContours(ArrayList<MatOfPoint> contours, List<MatOfPoint> possibleRect, List<MatOfPoint> possibleGoal) {
		double precision = 0.005;
		for (MatOfPoint mOP : contours) {
			MatOfPoint2f approxCurve = new MatOfPoint2f();
			Imgproc.approxPolyDP(new MatOfPoint2f(mOP.toArray()), approxCurve, precision * Imgproc.arcLength(new MatOfPoint2f(mOP.toArray()), true), true);
			MatOfPoint approxCurveMOP = new MatOfPoint();
			approxCurve.convertTo(approxCurveMOP, CvType.CV_32S);
			if (isRectangle(approxCurveMOP)) {
				possibleRect.add(approxCurveMOP);
			} else if (isGoal(approxCurveMOP)) {
				possibleGoal.add(approxCurveMOP);
			}
		}
		System.out.println("Number of potential goal lines: " + possibleGoal.size());
	}
	public static boolean isRectangle(MatOfPoint mOP) {
		if(mOP.toArray().length >= 4 && mOP.toArray().length <= 8) {
			return true;
		}
		return false;
	}
	public static boolean isGoal(MatOfPoint mOP) {
		if(Imgproc.contourArea(mOP) > 1200 && Imgproc.isContourConvex(new MatOfPoint(mOP.toArray())) && mOP.toArray().length >= 6 && mOP.toArray().length <= 20) {
			return true;
		}
		return false;
	}
	public static Mat blurOutput() {
		return blurOutput;
	}
	public static Mat rgbThresholdOutput() {
		return rgbThresholdOutput;
	}
	public static ArrayList<MatOfPoint> findContoursOutput() {
		return findContoursOutput;
	}
	public static ArrayList<MatOfPoint> convexHullsOutput() {
		return convexHullsOutput;
	}
	public static ArrayList<MatOfPoint> filterContoursOutput() {
		return filterContoursOutput;
	}
	enum BlurType {
		BOX("Box Blur"), GAUSSIAN("Gaussian Blur"), MEDIAN("Median Filter"), BILATERAL("Bilateral Filter");
		private final String label;
		BlurType(String label) {
			this.label = label;
		}
		public static BlurType get(String type) {
			if (BILATERAL.label.equals(type)) {
				return BILATERAL;
			} else if (GAUSSIAN.label.equals(type)) {
				return GAUSSIAN;
			} else if (MEDIAN.label.equals(type)) {
				return MEDIAN;
			} else {
				return BOX;
			}
		}
		@Override
		public String toString() {
			return this.label;
		}
	}
	/**
	 * Softens an image using one of several filters.
	 * @param input        The image on which to perform the blur.
	 * @param type         The blurType to perform.
	 * @param doubleRadius The radius for the blur.
	 * @param output       The image in which to store the output.
	 */
	private static void blur(Mat input, BlurType type, double doubleRadius, Mat output) {
		int radius = (int) (doubleRadius + 0.5);
		int kernelSize;
		switch (type) {
			case BOX:
			kernelSize = 2 * radius + 1;
			Imgproc.blur(input, output, new Size(kernelSize, kernelSize));
			break;
		case GAUSSIAN:
			kernelSize = 6 * radius + 1;
			Imgproc.GaussianBlur(input, output, new Size(kernelSize, kernelSize), radius);
			break;
		case MEDIAN:
			kernelSize = 2 * radius + 1;
			Imgproc.medianBlur(input, output, kernelSize);
			break;
		case BILATERAL:
			Imgproc.bilateralFilter(input, output, -1, radius, radius);
			break;
		}
	}
	/**
	 * Segment an image based on color ranges.
	 * 
	 * @param input  The image on which to perform the RGB threshold.
	 * @param red    The min and max red.
	 * @param green  The min and max green.
	 * @param blue   The min and max blue.
	 * @param out    The image in which to store the output.
	 */
	private static void rgbThreshold(Mat input, double[] red, double[] green, double[] blue, Mat out) {
		Imgproc.cvtColor(input, out, Imgproc.COLOR_BGR2RGB);
		Core.inRange(out, new Scalar(red[0], green[0], blue[0]), new Scalar(red[1], green[1], blue[1]), out);
	}
	/**
	 * Sets the values of pixels in a binary image to their distance to the
	 * nearest black pixel.
	 * 
	 * @param input    The image on which to perform the Distance Transform.
	 * @param type     The Transform.
	 * @param maskSize The size of the mask.
	 * @param output   The image in which to store the output.
	 */
	private static void findContours(Mat input, boolean externalOnly, List<MatOfPoint> contours) {
		Mat hierarchy = new Mat();
		contours.clear();
		int mode;
		if (externalOnly) {
			mode = Imgproc.RETR_EXTERNAL;
		} else {
			mode = Imgproc.RETR_LIST;
		}
		int method = Imgproc.CHAIN_APPROX_SIMPLE;
		Imgproc.findContours(input, contours, hierarchy, mode, method);
	}
	/**
	 * Compute the convex hulls of contours.
	 * 
	 * @param inputContours  The contours on which to perform the operation.
	 * @param outputContours The contours where the output will be stored.
	 */
	private static void convexHulls(List<MatOfPoint> inputContours, ArrayList<MatOfPoint> outputContours) {
		final MatOfInt hull = new MatOfInt();
		outputContours.clear();
		for (int i = 0; i < inputContours.size(); i++) {
			final MatOfPoint contour = inputContours.get(i);
			final MatOfPoint mopHull = new MatOfPoint();
			Imgproc.convexHull(contour, hull);
			mopHull.create((int) hull.size().height, 1, CvType.CV_32SC2);
			for (int j = 0; j < hull.size().height; j++) {
				int index = (int) hull.get(j, 0)[0];
				double[] point = new double[] { contour.get(index, 0)[0], contour.get(index, 0)[1] };
				mopHull.put(j, 0, point);
			}
			outputContours.add(mopHull);
		}
	}
	/**
	 * Filters out contours that do not meet certain criteria.
	 * 
	 * @param inputContours  The input list of contours.
	 * @param output         The output list of contours.
	 * @param minArea        The minimum area of a contour that will be kept.
	 * @param minPerimeter   The minimum perimeter of a contour that will be kept.
	 * @param minWidth       The minimum width of a contour.
	 * @param maxWidth       The maximum width of a contour.
	 * @param minHeight      The minimum height of a contour.
	 * @param maxHeight      The maximimum height of a contour.
	 * @param Solidity       The minimum and maximum solidity of a contour.
	 * @param minVertexCount The minimum vertex Count of the contours.
	 * @param maxVertexCount The maximum vertex Count of the contours.
	 * @param minRatio       The minimum ratio of width to height.
	 * @param maxRatio       The maximum ratio of width to height.
	 */
	private static void filterContours(List<MatOfPoint> inputContours, double minArea, double minPerimeter, double minWidth, double maxWidth, double minHeight, double maxHeight, double[] solidity, double maxVertexCount, double minVertexCount, double minRatio, double maxRatio, List<MatOfPoint> output) {
		final MatOfInt hull = new MatOfInt();
		output.clear();
		for (int i = 0; i < inputContours.size(); i++) {
			final MatOfPoint contour = inputContours.get(i);
			final Rect bb = Imgproc.boundingRect(contour);
			if (bb.width < minWidth || bb.width > maxWidth) {
				continue;
			}
			if (bb.height < minHeight || bb.height > maxHeight) {
				continue;
			}
			final double area = Imgproc.contourArea(contour);
			if (area < minArea) {
				continue;
			}
			if (Imgproc.arcLength(new MatOfPoint2f(contour.toArray()), true) < minPerimeter) {
				continue;
			}
			Imgproc.convexHull(contour, hull);
			MatOfPoint mopHull = new MatOfPoint();
			mopHull.create((int) hull.size().height, 1, CvType.CV_32SC2);
			for (int j = 0; j < hull.size().height; j++) {
				int index = (int) hull.get(j, 0)[0];
				double[] point = new double[] { contour.get(index, 0)[0], contour.get(index, 0)[1] };
				mopHull.put(j, 0, point);
			}
			final double solid = 100 * area / Imgproc.contourArea(mopHull);
			if (solid < solidity[0] || solid > solidity[1]) {
				continue;
			}
			if (contour.rows() < minVertexCount || contour.rows() > maxVertexCount) {
				continue;
			}
			final double ratio = bb.width / (double) bb.height;
			if (ratio < minRatio || ratio > maxRatio) {
				continue;
			}
			output.add(contour);
		}
	}
}