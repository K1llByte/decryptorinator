# TP5 Report

|        |             |
|:------:|:-----------:|
| A85272 | Jorge Mota  |
| A83840 | Maria Silva |

___

## First Part

In this part we had to solve 2 systems of congruences a) and b)

**Note:** We'll consider the defenition of a function `gcd(a,b)` that gives the <ins>greater common divisor</ins> of two values *a* and *b*.

The congruencies will be conversible to equations in the form:

`X ≣ a (mod b)`  ->  `X = b*k + a` , *k* being an positive integer

### **a )**

```
(1): X ≣ 48 (mod 13)
(2): X ≣ 57 (mod 23)
(3): X ≣ 39 (mod 27)
```

Firstly we begin with the congruency with largest modulus that is (3) `X ≣ 39 (mod 27)` 

Then we substitute this congruencies expression for *X* into the congruence with the next largest modulus (2):

```
27*m + 39 ≣ 57 (mod 23)
```

Solving this Linear Congruency ...

```
27*m ≣ 18 (mod 23)

note: gcd(27,23) = 1 so there is a solution

gcd(27,18) = 9

3*m ≣ 2 (mod 23)

3*m ≣ -21 (mod 23)

m ≣ -7 (mod 23)

m ≣ 16 (mod 23)

m = 23*k + 16
```

Replacing the expression form of this result in the expression for *X* we get:

```
X = 27*(23*l + 16) + 39
X = 621*l + 471
```

Then we replace this expression in the last congruency (1) and solve this Linear Congruency

```
621*l + 471 ≣ 48 (mod 13)

note: gcd(48,13) = 1 so there is a solution

621*l ≣ -423 (mod 13)

621*l ≣ 6 (mod 13)

207*l ≣ 2 (mod 13)

207*l ≣ -24 (mod 13)

gcd(24,207) = 3

69*l ≣ -8 (mod 13)

. . .

l ≣ 11 (mod 13)
```

Finally we replace this in the expression obtained previously and get the solution 
```
X ≣ 7302 (mod 8073)

X = 7302

```

### **b )**

## Second Part