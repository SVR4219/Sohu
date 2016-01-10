# Sohu

使用环境：
--------
Linux系统+python3

使用方法：
--------
1.将main.py拷入/usr/bin/文件夹中。
    sudo cp main.py /usr/bin

2.更改/usr/bin/main.py的使用权限。
    sudo chmod 744 main.py 或
    sudo chmod a+x main.py

3.直接输入命令运行。
    main.py    或
    main.py -d 60 -u http://m.sohu.com -o /tmp/backup

思路：
-------
1.脚本使用方式，直接使用main.py，故需要将main.py复制到/usr/bin作为本地应用。

2.抓取页面，下载html文件，再通过html文件中的资源链接作正则匹配，下载js,css,images等资源。

3.备份保存，将抓取页面以60秒为周期，按时间间隔保存于所给出的目录下，并将js,css,images等资源分别新建文件夹保存。

遇到问题：
-------
1.抓取页面时，需要根据后缀名进行正则匹配。但是在抓取图片时，由于图片有着多种不同的格式，可能会漏掉图片资源。解决办法是通过分析HTML文件中的<img>标签，找出页面所有图片格式。图片格式包括.jpg,.png

2.抓取到的页面与在浏览器访问的页面不一致，怀疑是反爬虫机制从中作梗。将爬虫加入HEADER伪装成火狐浏览器后，成功读取到与浏览器端相同的页面。后来的页面中，只有css文件和.png,.gif,.jpg三种格式的图片，没有js文件。

3.在编写过程中，最开始读取到的html文件是以byte编码。为了适应html文件的编码方式，后面的正则匹配也采取了同样的byte编码。但是，opener的op en方法只接收'str'类型变量，导致错误。解码为'ASCII'码方式即可。

4.main.py的参数读取方式，一开始是自己编写函数分析读取参数。但是功力不够，写出的代码又是循环又是嵌套判断。随后想到SHELL的参数读取，便想PYTHON或许会有标准模块来实现读取参数的功能。GOOGLE之后，采用了getopt模块实现。
