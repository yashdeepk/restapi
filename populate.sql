
INSERT INTO users(username, password) VALUES ('yashdeep', 'password123');
INSERT INTO users(username, password) VALUES ('tester', 'tester123');
INSERT INTO users(username, password) VALUES ('test', 'test');
INSERT INTO users(username, password) VALUES ('david', 'abc');


INSERT INTO forums(name, creator) VALUES ('sample forum', 'yashdeep');
INSERT INTO forums(name, creator) VALUES ('lets try', 'tester');
INSERT INTO forums(name, creator) VALUES ('what we need to do', 'david');

INSERT INTO threads(forum_id, title, text, author, timestamp) VALUES (1, 'this is first try', 'how you do that', 'tester', date('now'));
INSERT INTO threads(forum_id, title, text, author, timestamp) VALUES (1, 'this is second try', 'how backend works', 'david', date('now'));
INSERT INTO threads(forum_id, title, text, author, timestamp) VALUES (2, 'try once more lets see', 'how to do software testing', 'test', date('now'));
INSERT INTO threads(forum_id, title, text, author, timestamp) VALUES (2, 'again a try hope it works', 'how to do scrum meeting', 'yashdeep', date('now'));
INSERT INTO threads(forum_id, title, text, author, timestamp) VALUES (2, 'what to do next', 'just take rest and enjoy', 'david', date('now'));

INSERT INTO posts(thread_id, text, poster, timestamp) VALUES (1, 'i hope this post works', 'david', date('now'));
INSERT INTO posts(thread_id, text, poster, timestamp) VALUES (1, 'lets give it another try', 'david', date('now'));
INSERT INTO posts(thread_id, text, poster, timestamp) VALUES (1, 'i know what you mean it should work', 'yashdeep', date('now'));
INSERT INTO posts(thread_id, text, poster, timestamp) VALUES (1, 'i am not sure though', 'yashdeep', date('now'));
