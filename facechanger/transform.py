import cv2
import numpy as np

def get_triangulation_indices(points):
    """Get indices triples for every triangle
    """
    # Bounding rectangle
    bounding_rect = (*points.min(axis=0), *points.max(axis=0))
    # Triangulate all points
    subdiv = cv2.Subdiv2D(bounding_rect)
    for p in points:
        try:
            subdiv.insert([p])
        except Exception:
            pass
    # Iterate over all triangles
    for x1, y1, x2, y2, x3, y3 in subdiv.getTriangleList():
        # Get index of all points
        yield [(points==point).all(axis=1).nonzero()[0][0] for point in [(x1,y1), (x2,y2), (x3,y3)]]

def crop_to_triangle(img, triangle):
    """Crop image to triangle
    """
    # Get bounding rectangle
    bounding_rect = cv2.boundingRect(triangle)
    # Crop image to bounding box
    img_cropped = img[bounding_rect[1]:bounding_rect[1] + bounding_rect[3],
                      bounding_rect[0]:bounding_rect[0] + bounding_rect[2]]
    # Move triangle to coordinates in cropped image
    triangle_cropped = [(point[0]-bounding_rect[0], point[1]-bounding_rect[1]) for point in triangle]
    return triangle_cropped, img_cropped

def transform(src_img, src_points, dst_points): 
    """Transforms source image to target image, overwriting the target image.
    """
    dst_img = src_img.copy()

    for indices in get_triangulation_indices(src_points):
        try:
            # Get triangles from indices
            src_triangle = src_points[indices]
            dst_triangle = dst_points[indices]

            # Crop to triangle, to make calculations more efficient
            src_triangle_cropped, src_img_cropped = crop_to_triangle(src_img, src_triangle)
            dst_triangle_cropped, dst_img_cropped = crop_to_triangle(dst_img, dst_triangle)

            # Calculate transfrom to wrap from old image to new
            transform = cv2.getAffineTransform(np.float32(src_triangle_cropped), np.float32(dst_triangle_cropped))

            # Warp image
            dst_img_warped = cv2.warpAffine(src_img_cropped, transform, (dst_img_cropped.shape[1], dst_img_cropped.shape[0]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

            # Create mask for the triangle we want to transform
            mask = np.zeros(dst_img_cropped.shape, dtype = np.uint8)
            cv2.fillConvexPoly(mask, np.int32(dst_triangle_cropped), (1.0, 1.0, 1.0), 16, 0);

            # Delete all existing pixels at given mask
            dst_img_cropped*=1-mask
            # Add new pixels to masked area
            dst_img_cropped+=dst_img_warped*mask
        except Exception as e:
            print("Error:", e)
    return dst_img
