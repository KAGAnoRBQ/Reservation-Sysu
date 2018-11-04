# Reservation-Sysu

关于数据库的设计
1. 主键统一叫 id 不要加前缀
2. 增加一个部门表？
3. id统一用bigint 不要使用bool 用tinyint 你以为真存一个位？ 后期加属性的时候 只有true和false很尴尬
4. gym表的 manager字段改为manager_id（user_id）吧 用manager算什么嘛 名字？重名咋整？

按照一下的sql来规范建表吧： <br>
参考 ./sql_create_table.sql <br>

关于 API 接口 <br>
参照 first_group_api.docx 来写吧 <br>


分页设计： <br>
    从url中传参 page(当前页数) limit（每页个数）<br>
    example: api/xxxx/xxx/query/?page=xx&limit=xx <br>
    返回 <br>
    { <br>
        "data": [],  //查询的数据 <br>
        "error_code": 0, <br>
        "message": "done", <br>
        "paging": { <br>
            "current": 1,  // 当前页 <br>
            "pages": 10,   // 总页数 <br>
            "records": 0   // 总记录数 <br>
        }, <br>
        "success": true <br>
    } <br>
