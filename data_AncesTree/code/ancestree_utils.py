import os
import numpy as np
import random
import cv2
from PIL import Image
from io import BytesIO
from functools import partial

def op_cv2_resize(img, size, interpolation=cv2.INTER_LINEAR):
    """
    Resizes an image using OpenCV while maintaining its original aspect ratio.
    The shorter side of the image is scaled to 'size', and the other side 
    is scaled proportionally.
    
    Parameters:
    -----------
    img : PIL.Image. The input image object.
    size : int. The target length for the shorter dimension of the image.
    interpolation : int. OpenCV interpolation method (e.g., cv2.INTER_LINEAR, cv2.INTER_CUBIC).
        Defaults to cv2.INTER_LINEAR.
        
    Returns:
    --------
    img        : PIL.Image. The resized image.
    op_info    : dict. Metadata about the resizing parameters (size, method, interpolation).
    """
    img = np.array(img, np.uint8)
    h, w = img.shape[:2]
    if h < w:
        newsize = (int(w * size / h), size)
    else:
        newsize = (size, int(h * size / w))
    img = cv2.resize(img, newsize, interpolation=interpolation)
    assert img.dtype == np.uint8
    img = Image.fromarray(img)
    
    # Metadata
    op_info = {
        'method': 'cv2',
        'before_size': (w, h),
        'after_size': newsize,
        'interpolation': interpolation,
    }
    return img, op_info

def op_pil_resize(img, size, interpolation=Image.BILINEAR):
    """
    Resizes an image using Pillow while maintaining its original aspect ratio.
    The shorter side of the image is scaled to 'size', and the other side 
    is scaled proportionally.
    
    Parameters:
    -----------
    img : PIL.Image. The input image object.
    size : int. The target length for the shorter dimension of the image.
    interpolation : int. Pillow interpolation method (e.g., Image.BILINEAR, Image.BICUBIC).
        Defaults to Image.BILINEAR.
        
    Returns:
    --------
    img        : PIL.Image. The resized image.
    op_info    : dict. Metadata about the resizing parameters (size, method, interpolation).
    """
    w, h = img.size
    if h < w:
        newsize = (int(w * size / h), size)
    else:
        newsize = (size, int(h * size / w))
    img = img.resize(newsize, interpolation)
    
    # Metadata
    op_info = {
        'method': 'pil',
        'before_size': (w, h),
        'after_size': newsize,
        'interpolation': interpolation,
    }
    return img, op_info

def op_cv2_jpg(img, qf):
    """
    Performs JPEG compression on an image using OpenCV.
    
    Parameters:
    -----------
    img : PIL.Image. The input image object.
    qf  : int or str. The quality factor for JPEG compression (0-100).

    Returns:
    --------
    img        : PIL.Image. The compressed image.
    op_info    : dict. Metadata about the compression parameters.
    webp_bytes : bytes. The raw compressed byte stream (ready to be written to a .jpg file).
    """
    img_cv2 = np.array(img)[:,:,::-1]
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), int(qf)]
    result, encimg = cv2.imencode('.jpg', img_cv2, encode_param)
    decimg = cv2.imdecode(encimg, cv2.IMREAD_COLOR)
    
    # Metadata
    op_info = {
        'format': 'jpeg',
        'quality': qf,
        'method': 'cv2',
    }
    return Image.fromarray(decimg[:,:,::-1]), op_info, encimg

def op_pil_jpg(img, qf):
    """
    Performs JPEG compression on an image using Pillow.
    
    Parameters:
    -----------
    img : PIL.Image. The input image object.
    qf  : int or str. The quality factor for JPEG compression (0-100).

    Returns:
    --------
    img        : PIL.Image. The compressed image.
    op_info    : dict. Metadata about the compression parameters.
    webp_bytes : bytes. The raw compressed byte stream (ready to be written to a .jpg file).
    """
    with BytesIO() as out:
        img.save(out, format='jpeg', quality=int(qf))
        jpeg_bytes = out.getvalue()
        out.seek(0)
        img = Image.open(out)
        img.load()
        
    # Metadata
    op_info = {
        'format': 'jpeg',
        'quality': qf,
        'method': 'pil',
    }
    return img, op_info, jpeg_bytes

def op_pil_webp(img, qf):
    """
    Performs WebP compression on an image using Pillow.
    
    Parameters:
    -----------
    img : PIL.Image. The input image object.
    qf  : int or str. The quality factor for WebP compression (0-100).

    Returns:
    --------
    img        : PIL.Image. The compressed image.
    op_info    : dict. Metadata about the compression parameters.
    webp_bytes : bytes. The raw compressed byte stream (ready to be written to a .webp file).
    """
    with BytesIO() as out:
        img.save(out, format='WEBP', quality=int(qf))
        webp_bytes = out.getvalue()
        out.seek(0)
        img = Image.open(out)
        img.load()
        
    # Metadata
    op_info = {
        'format': 'webp',
        'quality': qf,
        'method': 'pil',
    }
    return img, op_info, webp_bytes

def op_pil_randomcrop_oneside(img, factor):
    """
    Performs a random crop on an image, reducing only one dimension (width or height) 
    by a given factor, while maintaining a minimum size of 256 pixels.
    
    Parameters:
    -----------
    img    : PIL.Image. The input image.
    factor : float. The scaling factor (0.0 to 1.0) to apply to the chosen side.

    Returns:
    --------
    cropped_img : PIL.Image. The resulting cropped image.
    op_info     : dict. Metadata about the crop (coordinates, dimensions, side affected).
    """
    w, h = img.size
    
    if random.random() < 0.5:
        w_fact = factor
        h_fact = 1.0
        cropped_side = 'w'
    else:
        w_fact = 1.0
        h_fact = factor
        cropped_side = 'h'
    
    new_w = max(int(w * w_fact), min(w,256))  # never smaller than 256
    new_h = max(int(h * h_fact), min(h,256))  # never smaller than 256
    
    # mu_left/top: The center of the available slack space
    mu_left = (w - new_w)/2.0
    sigma_left = mu_left/4.0
    mu_top = (h - new_h)/2.0
    sigma_top = mu_top/4.0
    
    # Sample from Gaussian distribution, to stay close enough to the center
    left = int(np.clip(random.gauss(mu_left, sigma_left), 0, w - new_w))
    top  = int(np.clip(random.gauss(mu_top, sigma_top), 0, h - new_h))
    right  = left + new_w
    bottom = top + new_h
    
    # Metadata
    op_info = {
        'factor': factor,
        'actual_factor': min(new_w/w, new_h/h),
        'cropped_side': cropped_side,
        'top': top,
        'left': left,
        'right': right,
        'bottom': bottom,
        'before_size': (w, h),
        'after_size': (new_w, new_h),
    }
    return img.crop((left, top, right, bottom)), op_info


def op_no(img):
    return img

def get_preop(typ, verbose=False):
    """
    Function that maps operation strings to post-processing functions.
    
    Parameters:
    -----------
    typ     : str. The operation identifier (e.g., 'cv2jpg_90', 'pilres_512').
    verbose : bool. If True, prints details about the selected operation and parameters.

    Returns:
    --------
    callable: A partial function ready to accept an image as its only/primary argument.
    """
    if typ == 'none':
        return op_no
    
    elif typ.startswith('cv2jpg'): # e.g., cv2jpg_75
        qf = int(typ[7:])
        if verbose:
            print('CV2 JPEG:', qf)
        return partial(op_cv2_jpg, qf=qf)
    
    elif typ.startswith('piljpg'): # e.g., piljpg_75
        qf = int(typ[7:])
        if verbose:
            print('PIL JPEG:', qf)
        return partial(op_pil_jpg, qf=qf)
    
    elif typ.startswith('pilwebp'): # e.g., pilwebp_75
        qf = int(typ[8:])
        if verbose:
            print('PIL WEBP:', qf)
        return partial(op_pil_webp, qf=qf)
    
    elif typ.startswith('cv2res'): # e.g., cv2res_512
        size = int(typ[7:])
        interpolation = random.choice([cv2.INTER_LINEAR, cv2.INTER_CUBIC, cv2.INTER_LANCZOS4])
        if verbose:
            print('resize:', size, interpolation)
        return partial(op_cv2_resize, size=size, interpolation=interpolation)
    
    elif typ.startswith('pilres'): # e.g., pilres_512
        size = int(typ[7:])
        interpolation = random.choice([Image.BILINEAR, Image.BICUBIC, Image.LANCZOS])
        if verbose:
            print('resize:', size, interpolation)
        return partial(op_pil_resize, size=size, interpolation=interpolation)
    
    elif typ.startswith('crop'): # e.g., crop_71.9
        factor = np.round(float(typ[5:]) / 100.0, 3)
        if verbose:
            print('crop:', factor)
        return partial(op_pil_randomcrop_oneside, factor=factor)
                  
    else:
        print('error', typ)
        assert False
        

# Distribution of QFs of real-world dataset
QFs = np.load('ReWIND_QFs.npy')

# Operation pipeline for single branch
def op_pipeline():
    """
    Planning the pipeline (operation types + parameters) in a string format
    
    Returns:
    --------
    pipeline : str. A list of dictionaries containing the full metadata of the tree.
    """
    
    pipeline = ['crop','resize','compress']
    probs = [0.5, 0.6, 0.95]
    ops = [x for x, p in zip(pipeline, probs) if random.random() < p]
    if len(ops)==0:
        ops = random.choices(pipeline, weights=probs)
    
    final_ops = []
    for op_type in ops:
                         
        # Defining cropping parameters
        if op_type == 'crop':
            lamb = 11.53
            y_sampled = np.random.exponential(scale=1.0/lamb)
            crop_ratio = np.clip(100 * np.exp(-y_sampled), 60, 99.9)
            final_ops.append(f'crop_{crop_ratio:04.1f}')  # min size 256
            
        # Defining resizing parameters
        elif op_type == 'resize':
            r = random.randint(256, 2048)
            res = random.choice(['pilres', 'cv2res'])
            final_ops.append(f'{res}_{r:03}')
            
        # Defining compression parameters
        elif op_type == 'compress':
            q = int(random.choice(QFs))
            jpg_type = ['piljpg', 'cv2jpg','pilwebp']
            p = [0.47, 0.46, 0.07]
            jpg = random.choices(jpg_type, weights=p)[0]
            final_ops.append(f'{jpg}_{q:03}')
            
    pipeline = ','.join(final_ops)
    return pipeline


def build_AncesTree(img, img_filename, current_savedir, out_basedir, seed=None, depth=4, level=0, branches=2, parent=None, log_rows=None, ops=None, save=True, verbose=False):
    """
    Recursively builds a degradation tree (AncesTree) starting from an input image.
    
    Each node in the tree corresponds to an image generated by applying one or more
    operations to the parent node.
    
    Parameters:
    -----------
    img             : PIL.Image or ndarray. The current image to be transformed.
    img_filename    : str. The original source filename of the root image.
    current_savedir : str. The directory path where the current level's results are stored.
    out_basedir     : str. The base directory for the entire transformation tree.
    seed            : int. Seed for reproducibility.
    depth           : int. Number of levels from current node.
    level           : int. The current depth level (0 being the root).
    branches        : int or list. Number of children per node. If list, must match depth.
    parent          : str. Path of the parent image that produced the current one.
    log_rows        : list. Accumulator for metadata dictionaries of all nodes.
    ops             : list. A list of operations already applied to reach this node.
    save            : bool. Whether to save image files and metadata to disk. If False, it only prints operations
    verbose         : bool. If True, prints transformation paths to console.

    Returns:
    --------
    log_rows        : list. A list of dictionaries containing the full metadata of the tree.
    """
            
    # Set the parent as the original filename for the root
    if level == 0:
        if seed is not None:
            random.seed(10)
        parent = img_filename
        log_rows = []
        ops = []
        
    if depth <= 0:
        return log_rows
        
    used_ops = set()  # To track operations at this level to ensure sibling branches are different
    if level == 0 and isinstance(branches, list):
        assert len(branches) == depth
    br = branches[level] if isinstance(branches, list) else branches
    
    for _ in range(br):
        # Generate a unique operation pipeline for this branch
        op = op_pipeline()
        while op in used_ops:
            op = op_pipeline()
        used_ops.add(op)
        
        # Keeping track of the full history of operations
        tot_ops = ops + [op]
        if verbose:
            print(tot_ops)
            
        new_img = None

        # Setup directory structure for this specific operation
        save_dir = os.path.join(current_savedir, op)
        if save:
            os.makedirs(save_dir, exist_ok=True)

            new_img = img.copy()
            op_dict = {}
            compression_bytes = None
            
            # Apply each individual operation in the string (e.g., 'piljpg_070, cv2res_512')
            for single_op in op.split(','):
                res = get_preop(single_op, verbose=False)(new_img)
                if len(res) == 3:
                    new_img, op_info, compression_bytes = res
                else:
                    new_img, op_info = res
                op_dict[single_op] = op_info
            
            # Saving the image (compressed vs PNG, to save space)
            save_path = os.path.join(save_dir, img_filename.split('/')[-1].split('.')[0])
            if compression_bytes is not None:
                ext = '.jpg' if 'jpg' in op else '.webp'
                save_path = save_path + ext
                with open(save_path, 'wb') as f:
                    f.write(compression_bytes)
            else:
                save_path = save_path + '.png'
                new_img.save(save_path, format="PNG")

            # Metadata for this node
            op_info_dict = {}
            op_info_dict['filename'] = save_path.replace(out_basedir,'')
            op_info_dict['parent'] = parent
            op_info_dict['src'] = img_filename
            op_info_dict['level'] = level+1  # cosi 0 e' la radice
            op_info_dict['op_node'] = op
            op_info_dict['op_tot'] = tot_ops
            op_info_dict['num_ops'] = len((',').join(tot_ops).split(','))
            op_info_dict['op_info'] = op_dict
            np.savez(os.path.splitext(save_path)[0] + ".npz", **op_info_dict)

            if level != 0:
                assert os.path.isfile(os.path.join(out_basedir, parent))
            
            w, h = new_img.size
            log_rows.append({
                "filename": op_info_dict['filename'],
                "parent": op_info_dict['parent'],
                "src": op_info_dict['src'],
                "level": op_info_dict['level'],
                "op_node": op_info_dict['op_node'],
                "op_tot": op_info_dict['op_tot'],
                "num_ops": op_info_dict['num_ops'],
                "w": w,
                "h": h,
                "size": w*h,
                "format": save_path.split('.')[-1],
            })

        # Recursion
        build_AncesTree(img=new_img, 
                img_filename=img_filename, 
                parent=op_info_dict['filename'],
                current_savedir=save_dir,
                out_basedir=out_basedir,
                seed=None, 
                depth=depth-1,
                level = level+1,
                branches=branches, 
                log_rows=log_rows, 
                ops=tot_ops, 
                save=save, 
                verbose=verbose)
    return log_rows

