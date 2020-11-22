# TP3 Report

This work has the objective to encrypt an image with both modes <ins>ECB</ins> and <ins>CBC</ins> and compare the visual result.

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

As we can see by the results the ECB encryption mode is not completly secure as we can check for patterns of the original image

![img2](https://i.imgur.com/lV28eFw.png)

And the decryption was successful

![img3](https://i.imgur.com/6mm19wR.png)

# Using CBC

As we can see by the results the CBC encryption mode turns the encrypted image in a matriz of complete unreadable pixels

![img4](https://i.imgur.com/ueSYdX1.png)

And the decryption was successful

![img5](https://i.imgur.com/6mm19wR.png)

# Comparisson

With knowledge of the process behind this two encryption modes, we could predict this results, since the <ins>ECB</ins> mode ciphers every block independently, with this we can predict that the encrypted result could present patters of the original data, and this can be very easily observed with images

![img_ecb](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/ECB_encryption.svg/601px-ECB_encryption.svg.png)

On the other hand, the <ins>CBC</ins> mode uses the previous cipher block as the "initial vector" of the next iterations. 

This being, the result will seem a lot more random than the previous mode.

![img_cbc](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/CBC_encryption.svg/600px-CBC_encryption.svg.png)