<?php 
	/*
 		* 作者：胡安延
		*time：2013－8－28
 		* 描述：数据库操作 类
 		* 更新：2013-9 -11  
		* 更新： 2013-10-8  单例
	*/
class Db{
	private static $conn="";
	private static $ip='localhost';
	private static $port=3306;
	private static $user='root';
	private static $passwd='root';
	
	//连接数据库
	static function connect($dbName='test'){
		if(self::$conn==""){		
			self::$conn = mysql_connect(Db::$ip.':'.Db::$port,Db::$user,DB::$passwd);
			mysql_select_db($dbName);
			mysql_query("set names utf8",self::$conn);
			is_resource(self::$conn) ? self::$conn : FALSE;
		}
	}
	
	//查询数据
	static function select($sql){
		$res=mysql_query($sql);
		if(is_resource($res)){
			$arr=array();
			while($row=mysql_fetch_assoc($res)){
				$arr[]=$row;
			}
			return $arr;
		} else return FALSE;
		
	}
	
	//增删改
	static function dml($sql){
		mysql_query($sql);
		if(mysql_affected_rows(self::$conn)>0) return TRUE;
		else return FALSE;
	}
	
	//增加，传值为表名和一维关联数组，下标为字段名，和值对应
	//成功则返回插入行的主键ID，否则返回FALSE
	static function insert($tbName,$arr){
		$fieldList="";  //字段名字符串
		$valueList="";  //插入值字符串
		foreach($arr as $key=>$value){
			$fieldList.=",".$key;
			$valueList.=",'".$value."'";
		}
		$fieldList=substr($fieldList,1);
		$valueList=substr($valueList,1);
		//合成sql语句
		$sql="insert into $tbName($fieldList) values($valueList)";
		mysql_query($sql);
		if(mysql_affected_rows(self::$conn)>0) return mysql_insert_id();    //成功则获取主键ID
		else return FALSE;
	}
	
	//通过主键删除，传值为表名和一维数组，下标为主键名，和值对应
	static  function delete($tbName,$arr){
		foreach ($arr as $key=>$value)
			$sql="delete from $tbName where $key='$value' ";
		mysql_query($sql);
		if(mysql_affected_rows(self::$conn)>0) return TRUE;
		else return FALSE;
	}
	
	//通过主键修改，下标为表名、一维数组（修改的键名=>键值，主键名=>键值）和主键名
	static function update($tbName,$arr,$primaryName){
		$where="$primaryName='".$arr[$primaryName]."'";
		unset($arr[$primaryName]);
		$set="";
		foreach ($arr as $key=>$value){
			$set.=",$key='$value'";
		}
		$set=substr($set,1);
		$sql="update $tbName set $set where $where";
		mysql_query($sql);
		if(mysql_affected_rows(self::$conn)>0) return TRUE;
		else return FALSE;
	}
	
	//关闭数据库
	static function close(){
		mysql_close(self::$conn);
	}
	
	//错误信息
	static function error(){
		return mysql_error();
	}
	
	
}


?>
