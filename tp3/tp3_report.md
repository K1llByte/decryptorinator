# TP3 Report

This work has the objective to encrypt an image with both modes <ins>EBC</ins> and <ins>CBC</ins> and compare the visual result.

For that we created a python script to easily encrypt and decrypt images using these modes

The file used for testing was a bmp image of a chess board pattern (`ex1.bmp`).

![img1](https://i.imgur.com/hfYBqHI.png)

```bash
python3 image_encrypt.py
```

Encrypting this file results in an unreadable file because the bmp image metadata is also encrypted, so we execute the following command to visualize the content of it:

**Note:** The encrypted image will be stored in `ex1.enc.bmp` and the decrypted image will be stored in `ex1.dec.bmp` 

```bash
dd if=ex1.bmp of=ex1.enc.bmp bs=1 count=54 conv=notrunc
```

# Using ECB

As we can see by the results the EBC encryption mode is not completly secure as we can check for patterns of the original image

![img2](https://i.imgur.com/lV28eFw.png)

And the decryption was successful

![img3](https://i.imgur.com/6mm19wR.png)

# Using CBC

As we can see by the results the CBC encryption mode turns the encrypted image in a matriz of complete unreadable pixels

![img4](https://i.imgur.com/ueSYdX1.png)

And the decryption was successful

![img5](https://i.imgur.com/6mm19wR.png)