---
title: WRITUP FOR CTF CHALLENGE
date: 2019-04-15
tags: CTF,HACKING
thumbnail: img/ctf.jpeg 
summary: A CTF Challenge writup
slug: haxx101
---
# Draw with us

Come draw with us!  
  
http://167.172.165.153:60000/  
  
Author: stackola

**Hint!**  Changing your color is the first step towards happiness.

## Solution

We were first greeted with an screen with an pixelated drawing board and an login form 
we can register with any name other than hacktm .
looking at the given source file we can see that it is checking.

`u.username.toUpperCase() !== config.adminUsername.toUpperCase()`
our inputted username in uppercase is not equal to 'HACKTM'.

Also to get the ability to change color and rights it checks that 
`u.username.toLowerCase() == config.adminUsername.toLowerCase()`.

To bypass this we found and unicode character ( `K`) which when converted to uppercase stays the same as `K` but when converted to lowercase becomes `k` .

hence now we are able to change our color and our rights (which basically are the stuff displayed on the api call to `/serverInfo`

next we need to send an request to /Updateuser with post parameter
##### `{"color": ,"rights":}`

if we send an request to the endpoint `/init` it sends an token with admin signature and a id calculated by 3 values n,p and .


`app.post("/init", (req, res) => {`<br>
`let { p = "0", q = "0", clearPIN } = req.body;`<br>
  `let target = md5(config.n.toString());`<br>
  `let pwHash = md5(`<br>
   ` bigInt(String(p)).multiply(String(q)).toString());`<br>
  `if (pwHash == target && clearPIN === _clearPIN) {`<br>
   ` // Clear the board`<br>
`    board = new Array(config.height)`<br>
    `  .fill(0)`<br>
      `.map(() => new Array(config.width).fill(config.backgroundColor));`<br>
    `boardString = boardToStrings();`<br>

   ` io.emit("board", { board: boardString });`<br>
  `}`<br>
So we try to get the values of n to get the admin token id value to 0 to get the flag
if we are able to set n as one of our rights we will be able to send and request to /init with the proper values and get the admin token
but the problem here was that n p and port was blacklisted 
hence to bypass this we send it as an array
ie:
`{"color": "0xDEDBEE","rights": [['n']]}`

As in javascript 
`dict = {'key': 'value'}`
```
A['key'] ==>'value'
and also 
A[['key']] ==> 'value'
```
hence we can get the value for n 
giving p the same values as n and q as 1 and make the admin token id equal to 0
change our token to the newly acquired token and visit /flag we get the flag
