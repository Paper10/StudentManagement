const express = require('express');
const session = require('express-session');
const fs = require('fs');
const app = express();
const path = require('path');

const classes = ['A', 'B', 'C']
const member = [
  {
    username : '학생1',
    password : 'stu1',
    class : 'A'
  },
  {
    username : '학생2',
    password : 'stu2',
    class : 'A'
  },
  {
    username : '학생3',
    password : 'stu3',
    class : 'B'
  },
  {
    username : '학생4',
    password : 'stu4',
    class : 'B'
  },
  {
    username : '학생5',
    password : 'stu5',
    class : 'C'
  },
  {
    username : '학생6',
    password : 'stu6',
    class : 'C'
  },
  {
    username : '교사1',
    password : 't1',
    class : 'T'
  }
]

// express-session 미들웨어 등록
app.use(express.static('views'));
app.use(session({
  secret: 'key',
  resave: false
}));

// JSON 형태의 요청 바디를 파싱하기 위한 미들웨어 등록
app.use(express.urlencoded({ extended: true }));

app.get('/', (req,res) => {
  res.render(path.join(__dirname + '/views/login.ejs'), {message: ' '});
});

// POST /login 요청 핸들러
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  console.log(username,password);

  // 사용자 인증 로직
  for(let i = 0;i<=member.length;i++){
    if ( i === member.length){  
      res.render(path.join(__dirname + '/views/login.ejs'), {message: 'Invalid username or password'});
      break;
    }
    if (username === member[i].username && password === member[i].password) {
    // 로그인 성공시 세션에 사용자 정보 저장
      req.session.user = {
       username: member[i].username,
       class : member[i].class
      };
      res.redirect('/main');
      break;
    }
  }
});

// GET /main 요청 핸들러
app.get('/main', (req, res) => {
  // 세션에 사용자 정보가 있는 경우에만 메인 페이지 반환
  if (req.session.user) {
    res.locals.user = req.session.user;
    if (req.session.user.class === 'T'){
      var sendlist = { };
      for(let i = 0;i<classes.length;i++){
        const class_data = fs.readFileSync(classes[i], 'utf-8');
        const class_arr = class_data.split('#');
        sendlist[classes[i]] = class_arr;
      }
      res.render(path.join(__dirname + '/views/main_teacher.ejs'), sendlist);
    } else {
      const class_data = fs.readFileSync(req.session.user.class, 'utf-8');
      const class_arr = class_data.split("#");
      console.log(class_arr)
      const class_word = fs.readFileSync(req.session.user.class + '.txt', 'utf-8');
      res.render(path.join(__dirname + '/views/main_student.ejs'), {
        progress : class_arr[0],
        number : class_arr[1],
        word : class_word
      });
    }
  } else {
    res.redirect('/');
  }
});

app.get('/submit/:arr', (req,res) => {
  const { arr } = req.params;
  const content = '#' + arr.split(',').slice(1).join('#');
  fs.appendFileSync(arr[0], content)
  res.send("OK");
});

app.get('/reset/:message', (req,res) => {
  const { message } = req.params;
  const arr = message.split(',');
  const data = arr.slice(1).join('#');
  fs.writeFileSync(arr[0],data);
  console.log(arr,data);
  res.send("OK");
});

app.get('/image/:cls', (req,res) => {
  const { cls } = req.params;
  res.send(cls + ".png");
});

// 서버 시작
app.listen(3000, () => {
  console.log('Server started on port 3000');
});
