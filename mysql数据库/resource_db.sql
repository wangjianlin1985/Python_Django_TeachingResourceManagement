/*
 Navicat Premium Data Transfer

 Source Server         : mysql5.6
 Source Server Type    : MySQL
 Source Server Version : 50620
 Source Host           : localhost:3306
 Source Schema         : resource_db

 Target Server Type    : MySQL
 Target Server Version : 50620
 File Encoding         : 65001

 Date: 26/07/2021 18:47:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_admin
-- ----------------------------
DROP TABLE IF EXISTS `t_admin`;
CREATE TABLE `t_admin`  (
  `username` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `password` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_admin
-- ----------------------------
INSERT INTO `t_admin` VALUES ('a', 'a');

-- ----------------------------
-- Table structure for t_collection
-- ----------------------------
DROP TABLE IF EXISTS `t_collection`;
CREATE TABLE `t_collection`  (
  `collectionId` int(11) NOT NULL AUTO_INCREMENT COMMENT '收藏id',
  `resourceObj` int(11) NOT NULL COMMENT '收藏的资源',
  `userObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '收藏用户',
  `collectTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '收藏时间',
  PRIMARY KEY (`collectionId`) USING BTREE,
  INDEX `resourceObj`(`resourceObj`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_collection_ibfk_1` FOREIGN KEY (`resourceObj`) REFERENCES `t_resource` (`resourceId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_collection_ibfk_2` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_collection
-- ----------------------------
INSERT INTO `t_collection` VALUES (1, 1, 'STU001', '2021-05-02 16:22:31');
INSERT INTO `t_collection` VALUES (2, 1, 'STU002', '2021-05-03 10:52:25');
INSERT INTO `t_collection` VALUES (3, 2, 'STU001', '2021-07-26 18:36:42');

-- ----------------------------
-- Table structure for t_leaveword
-- ----------------------------
DROP TABLE IF EXISTS `t_leaveword`;
CREATE TABLE `t_leaveword`  (
  `leaveWordId` int(11) NOT NULL AUTO_INCREMENT COMMENT '留言id',
  `leaveTitle` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言标题',
  `leaveContent` varchar(2000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言内容',
  `userObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '留言人',
  `leaveTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '留言时间',
  `replyContent` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '管理回复',
  `replyTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '回复时间',
  PRIMARY KEY (`leaveWordId`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_leaveword_ibfk_1` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_leaveword
-- ----------------------------
INSERT INTO `t_leaveword` VALUES (1, 'aaa', 'ddafa', 'STU001', '2021-05-02 16:22:54', 'fafas ', '2021-05-02 16:22:58');
INSERT INTO `t_leaveword` VALUES (2, 'ccc', 'ddd', 'STU001', '2021-05-02 21:54:26', '--', '--');

-- ----------------------------
-- Table structure for t_notice
-- ----------------------------
DROP TABLE IF EXISTS `t_notice`;
CREATE TABLE `t_notice`  (
  `noticeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '公告id',
  `title` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '标题',
  `content` varchar(5000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '公告内容',
  `publishDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`noticeId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_notice
-- ----------------------------
INSERT INTO `t_notice` VALUES (1, '教学资源网站开通了', '<p>老师可以在这里发布资料，学生们自己下载学习哦！</p>', '2021-05-02 16:23:10');
INSERT INTO `t_notice` VALUES (2, 'aaa', '<p>bbbb</p>', '2021-07-20 16:38:18');

-- ----------------------------
-- Table structure for t_resource
-- ----------------------------
DROP TABLE IF EXISTS `t_resource`;
CREATE TABLE `t_resource`  (
  `resourceId` int(11) NOT NULL AUTO_INCREMENT COMMENT '资源id',
  `resourceTypeObj` int(11) NOT NULL COMMENT '资源类型',
  `resourceName` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '资源名称',
  `resourcePhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '资源缩略图',
  `resourceDesc` varchar(8000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '资源介绍',
  `resourceFile` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '资料文件',
  `teacherObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '上传老师',
  `uploadTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '上传日期',
  `shenHeState` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '审核状态',
  `shenHeReply` varchar(800) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '审核回复',
  PRIMARY KEY (`resourceId`) USING BTREE,
  INDEX `resourceTypeObj`(`resourceTypeObj`) USING BTREE,
  INDEX `teacherObj`(`teacherObj`) USING BTREE,
  CONSTRAINT `t_resource_ibfk_1` FOREIGN KEY (`resourceTypeObj`) REFERENCES `t_resourcetype` (`typeId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_resource_ibfk_2` FOREIGN KEY (`teacherObj`) REFERENCES `t_teacher` (`teacherNo`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_resource
-- ----------------------------
INSERT INTO `t_resource` VALUES (1, 1, 'springsecurity+oatuh2.0+jwt入门到精通文档', 'img/1.jpg', '<h2><span lang=\"EN-US\">SpringSecurity</span></h2>\r\n<p><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Spring Security</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">是一个能够为基于</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Spring</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">的企业应用系统提供声明式的安全访问控制解决方案的安全框架。它提供了一组可以在</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Spring</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">应用上下文中配置的</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Bean</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">，充分利用了</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Spring IoC</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">，</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">DI</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">（控制反转</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">Inversion of Control ,DI:Dependency Injection </span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">依赖注入）和</span><span style=\"font-size: 10.5pt; font-family: \'Times New Roman\',\'serif\'; mso-fareast-font-family: 宋体; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\" lang=\"EN-US\">AOP</span><span style=\"font-size: 10.5pt; font-family: 宋体; mso-ascii-font-family: \'Times New Roman\'; mso-hansi-font-family: \'Times New Roman\'; mso-bidi-font-family: \'Times New Roman\'; mso-font-kerning: 1.0pt; mso-ansi-language: EN-US; mso-fareast-language: ZH-CN; mso-bidi-language: AR-SA;\">（面向切面编程）功能，为应用系统提供声明式的安全访问控制功能，减少了为企业系统安全控制编写大量重复代码的工作。</span></p>', 'file/spring-security.doc', 'TH001', '2021-05-02 16:22:06', '审核通过', '不错不错');
INSERT INTO `t_resource` VALUES (2, 3, '英语四级常用词汇 ', 'img/2.jpg', '<p>集合了常用的四级英语词汇，助你考四级顺利通关！</p>', 'file/四级词汇.doc', 'TH001', '2021-05-03 13:25:41', '审核通过', '好的');
INSERT INTO `t_resource` VALUES (3, 1, 'TCP/IP网络通信ppt', 'img/tcp.jpg', '<p>讲解了计算机之间如何通过tcp/ip通信的原理</p>', 'file/tcp-ip.ppt', 'TH002', '2021-05-04 00:59:31', '审核通过', 'good');
INSERT INTO `t_resource` VALUES (4, 1, '232', 'img/NoImage.jpg', '<p>aafa</p>', 'file/NoFile.jpg', 'TH001', '2021-05-04 01:01:09', '待审核', '--');
INSERT INTO `t_resource` VALUES (5, 1, 'gasfa', 'img/NoImage.jpg', '<p>afaaffafa</p>', 'file/NoFile.jpg', 'TH002', '2021-05-04 01:04:25', '待审核', '--');

-- ----------------------------
-- Table structure for t_resourcecomment
-- ----------------------------
DROP TABLE IF EXISTS `t_resourcecomment`;
CREATE TABLE `t_resourcecomment`  (
  `commentId` int(11) NOT NULL AUTO_INCREMENT COMMENT '评论id',
  `resourceObj` int(11) NOT NULL COMMENT '被评资源',
  `teacherObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '资源发布人',
  `commentScore` float NOT NULL COMMENT '评分',
  `content` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论内容',
  `userObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '评论用户',
  `commentTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '评论时间',
  PRIMARY KEY (`commentId`) USING BTREE,
  INDEX `resourceObj`(`resourceObj`) USING BTREE,
  INDEX `teacherObj`(`teacherObj`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_resourcecomment_ibfk_1` FOREIGN KEY (`resourceObj`) REFERENCES `t_resource` (`resourceId`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_resourcecomment_ibfk_2` FOREIGN KEY (`teacherObj`) REFERENCES `t_teacher` (`teacherNo`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_resourcecomment_ibfk_3` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_resourcecomment
-- ----------------------------
INSERT INTO `t_resourcecomment` VALUES (1, 1, 'TH001', 5, '11', 'STU001', '2021-05-02 16:22:23');
INSERT INTO `t_resourcecomment` VALUES (2, 1, 'TH001', 5, '非常不错的！', 'STU002', '2021-05-03 00:44:13');

-- ----------------------------
-- Table structure for t_resourcetype
-- ----------------------------
DROP TABLE IF EXISTS `t_resourcetype`;
CREATE TABLE `t_resourcetype`  (
  `typeId` int(11) NOT NULL AUTO_INCREMENT COMMENT '类型id',
  `typeName` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类型名称',
  `typeDesc` varchar(800) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '类型描述',
  PRIMARY KEY (`typeId`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_resourcetype
-- ----------------------------
INSERT INTO `t_resourcetype` VALUES (1, '计算机', '计算机技术相关');
INSERT INTO `t_resourcetype` VALUES (2, '电子技术', '电子技术的相关资料');
INSERT INTO `t_resourcetype` VALUES (3, '英语', '英语资料');

-- ----------------------------
-- Table structure for t_teachefollow
-- ----------------------------
DROP TABLE IF EXISTS `t_teachefollow`;
CREATE TABLE `t_teachefollow`  (
  `followId` int(11) NOT NULL AUTO_INCREMENT COMMENT '订阅id',
  `teacherObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '被订阅老师',
  `userObj` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '订阅人',
  `followTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '订阅时间',
  PRIMARY KEY (`followId`) USING BTREE,
  INDEX `teacherObj`(`teacherObj`) USING BTREE,
  INDEX `userObj`(`userObj`) USING BTREE,
  CONSTRAINT `t_teachefollow_ibfk_1` FOREIGN KEY (`teacherObj`) REFERENCES `t_teacher` (`teacherNo`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `t_teachefollow_ibfk_2` FOREIGN KEY (`userObj`) REFERENCES `t_userinfo` (`user_name`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_teachefollow
-- ----------------------------
INSERT INTO `t_teachefollow` VALUES (1, 'TH001', 'STU001', '2021-05-02 16:22:38');
INSERT INTO `t_teachefollow` VALUES (2, 'TH001', 'STU002', '2021-05-03 11:47:35');
INSERT INTO `t_teachefollow` VALUES (3, 'TH002', 'STU001', '2021-07-26 18:37:14');

-- ----------------------------
-- Table structure for t_teacher
-- ----------------------------
DROP TABLE IF EXISTS `t_teacher`;
CREATE TABLE `t_teacher`  (
  `teacherNo` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'teacherNo',
  `password` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `sex` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别',
  `birthDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '出生日期',
  `teacherPhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '老师照片',
  `zhicheng` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '职称',
  `telephone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `comeDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '入职日期',
  `address` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '家庭地址',
  `teacherDesc` varchar(5000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '老师介绍',
  PRIMARY KEY (`teacherNo`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_teacher
-- ----------------------------
INSERT INTO `t_teacher` VALUES ('TH001', '123', '王喜天', '男', '2021-05-03', 'img/12.jpg', '高级讲师', '13598239834', '2021-05-02', '四川南充', '<p>10几年教学经验！</p>');
INSERT INTO `t_teacher` VALUES ('TH002', '123', '王立国', '男', '2021-05-04', 'img/3.jpg', '教授', '13958209342', '2021-05-02', '四川巴中', '<p>教学认真负责，经验丰富</p>');

-- ----------------------------
-- Table structure for t_userinfo
-- ----------------------------
DROP TABLE IF EXISTS `t_userinfo`;
CREATE TABLE `t_userinfo`  (
  `user_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'user_name',
  `password` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '登录密码',
  `className` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '所在班级',
  `name` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '姓名',
  `gender` varchar(4) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '性别',
  `birthDate` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '出生日期',
  `userPhoto` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '用户照片',
  `telephone` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `address` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '家庭地址',
  `regTime` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '注册时间',
  `userState` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '账号状态',
  PRIMARY KEY (`user_name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of t_userinfo
-- ----------------------------
INSERT INTO `t_userinfo` VALUES ('STU001', '123', '计算机3班', '张晓彤', '女', '2021-05-11', 'img/1THGT2-9.jpg', '13058129342', 'dashn@126.com', '四川成都春熙路', '2021-05-02 16:19:28', '正常');
INSERT INTO `t_userinfo` VALUES ('STU002', '123', '计算机4班', '李小兔', '女', '2021-05-01', 'img/9.jpg', '13598013942', 'xiaotu@163.com', '四川 达州', '2021-07-20 16:12:39', '正常');

SET FOREIGN_KEY_CHECKS = 1;
