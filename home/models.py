import random
from post.models import Post, Comment
from user.models import MyUser, Conversation, Message


class ShiliEmail:
    def form_mail(self, url, content, email):
        form_mail = """
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                #index_login {
                    background-color: #5B7D87;
                    background-image: -webkit-linear-gradient(45deg, #91B3BC 50%, #5B7D87 50%);
                    height: 100%;
                    z-index: 0;
                    padding: 50px;
                    padding-top:0;
                }
        
                .btn-grad {
                    background-image: linear-gradient(to right, #FF512F 0%, #F09819 51%, #FF512F 100%);
                }
        
                .btn-grad {
                    margin: 20px auto;
                    padding: 15px 45px;
                    text-align: center;
                    text-transform: uppercase;
                    transition: 0.5s;
                    background-size: 200% auto;
                    color: #070000;
                    box-shadow: 0 0 10px #eee;
                    border-radius: 10px;
                    display: block;
                    font-weight: bold;
                }
        
                .btn-grad:hover {
                    background-position: right center;
                    color: #efefef;
                   
                }
        
                .welcome h1 {
                    font-family: "Segoe UI", serif;
                    font-style: italic;
                    font-size: 100px;
                    color: #FFFFFF;
                    font-weight: bold;
                }
        
                .welcome h2, .welcome a {
                    font-family: "Segoe UI", serif;
                    font-style: italic;
                    font-size: 35px;
                    color: #FFFFFF;
                    font-weight: bold;
                    text-decoration: none;
                }
        
                .welcome p {
                    text-align: right;
                    font-family: "Consolas", serif;
                    font-size: 35px;
                    color: #FFFFFF
                }
        
                h1 span {
                    font-family: 'Berkshire Swash', cursive;
                    font-weight: bold;
                    color: #F18E16;
                    font-size: 150px;
                    text-transform: capitalize;
                    font-style: normal;
                }
            </style>
        </head>
        <body>
        <div id="index_login">
            <div class="welcome ">
                <h1 class="col-12">WELCOME TO <span>Shili</span></h1>
                <p class="col-12">B???t tr???n kho???nh kh???c - D???n d???t xu h?????ng </p>
                <h2> Xin ch??o """ + email + """</h2>
                <a class="btn-grad" href=" """ + url + """ " >""" + content + """</a>
            </div>
        </div>
        </body>
             """
        return form_mail


class MaHoaOneTimePad:
    def __init__(self):
        self.charset = "v4b7zt9c8fwj5ok0.h6euqai1@lxrgd2yms_pn3".lower()
        # self.charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.".lower()

    def ma_hoa(self, plaintext):
        otp = "".join(random.sample(self.charset, len(self.charset)))
        result = ""
        for c in plaintext.lower():
            if c not in otp:
                continue
            else:
                result += otp[self.charset.find(c)]
        return otp, result

    def giai_ma(self, otp, secret):
        result = ""
        for c in secret.lower():
            if c not in otp:
                continue
            else:
                result += self.charset[otp.find(c)]
        return result


class Database:
    def __init__(self, userid):
        self.userid = str(userid)

    # L???y to??n b??? b??i ????ng c???a t??i kho???n ??ang theo d??i
    def get_post_index(self):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE (a.user_id IN(SELECT followres_id FROM user_follower WHERE main_user_id = " + self.userid + ") OR a.user_id = " + self.userid + ")  AND a.public != 'Ch??? M??nh T??i' ORDER BY a.created_at DESC"
        return Post.objects.raw(sql)

    # L???y ra th??ng tin 1 b??i vi???t v???i id c??? th???
    def get_post_id(self, post_id):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.post = '" + str(
            post_id) + "'"
        return Post.objects.raw(sql)

    #  Tr??? v??? json th??ng tin b??i vi???t
    def json_post(self, get_post):
        posts = []
        for i in get_post:
            thisdict = {}
            thisdict["post_id"] = i.post
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["feeling"] = i.feeling
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ng??y %m/%d/%Y")
            thisdict["public"] = i.public
            thisdict["content"] = i.content
            thisdict["hashtag"] = i.hashtag
            thisdict["user_id"] = i.user_id
            thisdict["avatar"] = str(i.avatar)
            thisdict["photo"] = str(i.photo)
            posts.append(thisdict)
        return posts

    # L???y ra th??ng tin b??i vi???t n???m trong top x hashtag n???i b???t
    def get_post_in_top_x_hashtag(self, limit):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id JOIN( SELECT hashtag,count(hashtag) AS SoLuot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC LIMIT " + limit + ") c ON a.hashtag =c.hashtag"
        return Post.objects.raw(sql)

    # L???y id b??i vi???t m???i ????ng g???n nh???t c???a t??i kho???n ????ng nh???p
    def get_id_new_post(self):
        sql = 'SELECT post From user_myuser a JOIN post_post b on a.id =  b.user_id ORDER BY created_at DESC LIMIT 1'
        return Post.objects.raw(sql)[0].post

    # L???y ra th??ng tin b??i vi???t cho hashtag b???t k??
    def get_post_hashtag(self, hashtag):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.hashtag = '" + hashtag + "'"
        return Post.objects.raw(sql)

    # L???y t??n hashtag v??  s??? l?????t xu???t hi???n trong top x hashtag
    def get_count_top_x_hashtag(self, limit):
        sql = "SELECT  hashtag,count(hashtag) AS soluot FROM post_post GROUP BY hashtag  ORDER BY soluot DESC"
        count_top_x_hashtag = []
        for i in Post.objects.raw(sql)[0:limit]:
            thisdict = {}
            thisdict["hashtag"] = i.hashtag
            thisdict["soluot"] = i.soluot
            count_top_x_hashtag.append(thisdict)
        return count_top_x_hashtag

    # tr??? v??? t???t c??? comments c???a b??i vi???t v???i post_id
    def get_comment_post_id(self, post_id):
        sql = "SELECT * FROM post_comment a JOIN user_myuser b ON  a.user_id = b.id WHERE a.post_id =" + str(
            post_id)
        comment_post_id = []
        for i in Comment.objects.raw(sql):
            thisdict = {}
            thisdict["content"] = i.content
            thisdict["user_id"] = i.user_id
            thisdict["username"] = i.username
            thisdict["comment_id"] = i.comment
            thisdict["fullname"] = i.first_name + i.last_name
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ng??y %m/%d/%Y")
            thisdict["post_id"] = i.post_id
            comment_post_id.append(thisdict)
        return comment_post_id

    # tr??? v??? to??n b??? th??ng tin ng?????i d??ng v???i username
    def get_profile(self, username):
        sql = "SELECT * FROM user_myuser a WHERE a.username ='" + str(username) + "'"
        get_profile = MyUser.objects.raw(sql)
        profile = []
        for i in get_profile:
            thisdict = {}
            thisdict["username"] = i.username
            thisdict["user_id"] = i.id
            thisdict["email"] = i.email
            thisdict["avatar"] = str(i.avatar)
            thisdict["cover_image"] = str(i.cover_image)
            thisdict["first_name"] = i.first_name
            thisdict["last_name"] = i.last_name
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["birthday"] = i.birthday
            thisdict["gender"] = i.gender
            thisdict["address"] = i.address
            thisdict["intro"] = i.intro
            thisdict["date_joined"] = i.date_joined.strftime("%H:%M:%S ng??y %m/%d/%Y")
            thisdict["is_superuser"] = i.is_superuser
            profile.append(thisdict)
        return profile

    # L???y ra t???t c??? b??i vi???t c???a username nh???p v??o
    def get_profile_posts(self, username, session_user):
        if username != session_user:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + str(
                username) + "'  AND a.public != 'Ch??? M??nh T??i' ORDER BY created_at DESC"
        else:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + str(
                username) + "' ORDER BY created_at DESC"
        get_profile_posts = Post.objects.raw(sql)
        profile_posts = []
        for i in get_profile_posts:
            thisdict = {}
            thisdict["post_id"] = i.post
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["feeling"] = i.feeling
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ng??y %m/%d/%Y")
            thisdict["public"] = i.public
            thisdict["content"] = i.content
            thisdict["hashtag"] = i.hashtag
            thisdict["user_id"] = i.user_id
            thisdict["avatar"] = str(i.avatar)
            thisdict["photo"] = str(i.photo)
            profile_posts.append(thisdict)
        return profile_posts

    # Chuy???n ?????i username th??nh id
    def username_convert_id(self, username):
        user_id_sql = "SELECT id FROM user_myuser WHERE username ='" + str(username) + "'"
        return MyUser.objects.raw(user_id_sql)[0].id

    # Chuy???n ?????i id th??nh username
    def id_convert_username(self, id):
        user_id_sql = "SELECT username FROM user_myuser WHERE id =" + str(id)
        return MyUser.objects.raw(user_id_sql)[0].username

    # l???y ra c??c t??i kho???n m?? username ??ang theo d??i
    def get_watching(self, username):
        user_id = self.username_convert_id(username)
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
            user_id) + ") b ON a.id = b.followres_id WHERE  a.id !='" + str(user_id) + "'"
        get_watching = MyUser.objects.raw(sql)
        profile_watching = []
        for i in get_watching:
            thisdict = {}
            thisdict["avatar"] = str(i.avatar)
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["id"] = i.id
            profile_watching.append(thisdict)
        return profile_watching

    # l???y ra c??c t??i kho???n ??ang theo d??i username (???????c theo d??i)
    def get_followed(self, username):
        user_id = self.username_convert_id(username)
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE followres_id ='" + str(
            user_id) + "') b ON a.id = b.main_user_id WHERE  a.id !='" + str(user_id) + "'"
        get_followed = MyUser.objects.raw(sql)
        profile_followed = []
        for i in get_followed:
            thisdict = {}
            thisdict["avatar"] = str(i.avatar)
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["id"] = i.id
            profile_followed.append(thisdict)
        return profile_followed

    # L???y t???t c??? ng?????i d??ng m?? t??i kho???n ????ng nh???p ch??a theo d??i
    def get_all_user(self):
        sql = "SELECT * FROM user_myuser WHERE id !=" + self.userid + " AND id NOT IN (SELECT followres_id FROM user_follower c WHERE c.main_user_id = " + self.userid + " ) Order by date_joined DESC"
        get_all_user = MyUser.objects.raw(sql)
        all_user = []
        for i in get_all_user:
            thisdict = {}
            thisdict["id"] = i.id
            thisdict["username"] = i.username
            thisdict["avatar"] = str(i.avatar)
            thisdict["full_name"] = i.first_name + " " + i.last_name
            all_user.append(thisdict)
        return all_user

    # ki???m tra xem ???? theo d??i ch??a
    def check_id_follow(self, user_1, user_2):
        sql = "SELECT f_id FROM user_follower WHERE main_user_id = " + str(
            user_1) + " AND followres_id =  " + str(user_2)
        if Conversation.objects.raw(sql)[:1]:
            return Conversation.objects.raw(sql)[:1][0].f_id
        else:
            return False

    # ki???m tra xem ???? c?? ph??ng chat ch??a
    def check_box_chat(self, user_1, user_2):
        sql = "SELECT c_id FROM user_conversation WHERE user_1_id = '" + str(user_1) + "' AND user_2_id = '" + str(
            user_2) + "' OR user_2_id =  '" + str(user_1) + "' AND user_1_id = '" + str(user_2) + "'"
        if Conversation.objects.raw(sql)[:1]:
            return Conversation.objects.raw(sql)[0:1][0].c_id
        else:
            return False

    # ?????m s???  tin nh???n c???a ph??ng chat
    def count_mess(self, id_room):
        sql = "SELECT COUNT(m_id) AS SoTin FROM user_conversation a JOIN user_message b ON a.c_id = b.conversation_id WHERE a.c_id =" + str(
            id_room)
        return Message.objects.raw(sql)[0:1][0].SoTin

    # l???y n???i dung chat c???a ph??ng chat
    def get_context_box_chat(self, id_room):
        sql = "SELECT * FROM user_message WHERE conversation_id =" + str(id_room)
        mess = Conversation.objects.raw(sql)
        context_box_chat = []
        for i in mess:
            thisdict = {}
            thisdict["from_user_id"] = i.from_user_id
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ng??y %m/%d/%Y")
            thisdict["content"] = i.content
            thisdict["m_id"] = i.m_id
            context_box_chat.append(thisdict)
        return context_box_chat
