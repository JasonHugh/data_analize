<?php
header("content-type:text/html;charset=utf-8");
require_once('db.class.php');
Db::connect();
if($_GET['get']=='count'){
	//获取一个用户的所有类别应用的安装数量
	$arr = Db::select('select distinct b.cate_name,c.male-c.famale imbus,count(distinct a.pack_id) cnt from user_pack a left join pack_cate b on a.pack_id=b.pack_id left join cate c on b.cate_name=c.cate_name  where uid=220132360 and b.cate_name is not null group by cate_name');
	echo json_encode($arr);
}else if($_GET['get']=='relation'){
	//获取这些类别之间的关系
	Db::dml('create table temp_relation as (select distinct cate_name from user_pack a left join pack_cate b on a.pack_id=b.pack_id where uid=220132360 and b.cate_name is not null)');
	$arr = Db::select('select cate1,cate2,relation from cate_relation where cate1 in (select * from temp_relation) and cate2 in (select * from temp_relation) order by id');
	Db::dml('drop table temp_relation');
	echo json_encode($arr);
}
?>