import os
import re
import fitz
import img2pdf


class FileUtil:
    @classmethod
    def mk_files(cls, root, tp):
        if not os.path.exists(root):
            os.mkdir(root)
        for i in range(10):
            name = str(i) + "." + tp
            with open(root + name, 'wb') as f:
                f.close()
                print(str(i) + "Done!")

    @classmethod
    def ren_files(cls, root, name, tp):
        f_list = os.listdir(root)
        for i in f_list:
            if i.split('.')[-1] == tp:
                os.rename(root + i, root + name + str(f_list.index(i)) + "." + tp)
        print(os.listdir(root))

    @classmethod
    def del_files(cls, root, tp):
        f_list = os.listdir(root)
        for i in f_list:
            if i.split('.')[-1] == tp:
                os.remove(root + i)
        print(os.listdir(root))

    @classmethod
    def img2pdf(cls, root, name):
        doc = fitz.open()
        img_list = os.listdir(root)
        img_list.sort(key=lambda x: int(x[:-4]))  # 确保按文件名排序
        for img in img_list:  # 读取图片
            img_path = root + '/' + img
            img_doc = fitz.open(img_path)  # 打开图片
            pdf_bytes = img_doc.convert_to_pdf()  # 使用图片创建单页的 PDF
            img_pdf = fitz.open("pdf", pdf_bytes)
            doc.insert_pdf(img_pdf)  # 将当前页插入文档
        pathname = root + '/' + name + '.pdf'
        if os.path.exists(pathname):
            os.remove(pathname)
        doc.save(pathname)  # 保存pdf文件
        doc.close()

    @classmethod
    def img2pdf2(cls, photo_path, name):
        # 生成地址列表
        photo_list = os.listdir(photo_path)
        photo_list = [os.path.join(photo_path, i) for i in photo_list]

        # 指定pdf的单页的宽和高
        inp = (img2pdf.mm_to_pt(1920), img2pdf.mm_to_pt(1080))
        layout_fun = img2pdf.get_layout_fun(inp)

        pdf_path = photo_path + '/' + name + '.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(img2pdf.convert(photo_list, layout_fun=layout_fun))

    @classmethod
    def pdf2pic(cls, path, pic_path):
        """
        # 从pdf中提取图片
        :param path: pdf的路径
        :param pic_path: 图片保存的路径
        :return:
        """

        # 使用正则表达式来查找图片
        check_xo = r"/Type(?= */XObject)"
        check_im = r"/Subtype(?= */Image)"

        # 打开pdf
        doc = fitz.open(path)

        # 图片计数
        img_count = 0
        len_xref = doc.xrefLength()

        # 打印PDF的信息
        print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), len_xref - 1))

        # 遍历每一个对象
        for i in range(1, len_xref):
            # 定义对象字符串
            text = doc.xrefObject(i)
            isXObject = re.search(check_xo, text)
            # 使用正则表达式查看是否是图片
            isImage = re.search(check_im, text)
            # 如果不是对象也不是图片，则continue
            if not isXObject or not isImage:
                continue
            img_count += 1
            # 根据索引生成图像
            pix = fitz.Pixmap(doc, i)
            # 根据pdf的路径生成图片的名称
            new_name = path.replace('\\', '_') + "_img{}.png".format(img_count)
            new_name = new_name.replace(':', '')

            # 如果pix.n<5,可以直接存为PNG
            if pix.n < 5:
                pix.writePNG(os.path.join(pic_path, new_name))
            # 否则先转换CMYK
            else:
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.writePNG(os.path.join(pic_path, new_name))
            # 释放资源
            print("提取了{}张图片".format(img_count))
