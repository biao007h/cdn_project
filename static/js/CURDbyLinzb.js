   $(function () {
    function initTable(pager){
        // pager：提取第pager页的数据
        $.ajax({
                    url:requestURL,
                    type:'GET',
                    data:{'pager':pager},
                    dataType:'Json',
                    success:function (arg) {
                        initchoice(arg.choices_dict)
                        initThead(arg.fields_config)
                        initTbody(arg.data,arg.fields_config)
                    }
        })
    }
    function initThead(field) {
        tr_ele=$("<tr></tr>")
        $.each(field,function (k,v) {
                if(v["display"]){
                    th_ele=$("<th></th>")
                    th_ele.text(v["field_name"])
                    tr_ele.append(th_ele)
                }
                $("#table_th").append(tr_ele)
            })

    }
    function initTbody(data,field) {
        // save按钮重载时，会重新生成，所以需清空
         $('#table_td').empty();
        // 数据展示一般做法是，取出展示的字段，然后循环数据列表判断是否在里面，有则展示
        // 但是这么做有个缺点是数据和字段的顺序要对应(因为是以数据为顺序，而字段顺序是可能变化的)，而且不利于扩展
        // 这里采用先循环数据列表，再循环field字段列表，根据字段的列表的顺序反选查找赋值
        // 缺点是多次循环field比较耗性能，但是扩展能力变强了
        $.each(data,function (data_k,data_v) {
            tr_ele=$("<tr></tr>")
            // tr赋值属性，标记当前行在数据库中的id，为更新做旧数据标记
            var old_data_id=data_v["id"]
            tr_ele.attr("old_data_id",old_data_id)
            $.each(field,function (field_k,field_v) {
                if(field_v.display){
                    td_ele=$("<td></td>")
                    // td 赋值attr
                    // 赋值field_in_db属性，用以在更新时找到对应数据库字段
                    td_ele.attr("field_in_db",field_v["field_in_db"])
                    $.each(field_v.attr,function (attr_k,attr_v) {
                            // "origin_v":"@field_name",属性赋值需转为数据库的值
                            if(attr_k==="origin_v")
                            {
                                attr_v=data_v[field_v["field_in_db"]]
                                td_ele.attr(attr_k,attr_v)
                            }else{
                                td_ele.attr(attr_k,attr_v)
                            }
                    })
                    if(field_v["show_data"][0]==='@'){
                        td_ele.html(data_v[field_v["field_in_db"]])
                    }
                    else if(field_v["show_data"][0]==='!'){
                        var f_v=field_v["show_data"]
                        var choice_list=f_v.substring(1,f_v.length)
                        var choice_v=value_from_choice_list(data_v[field_v["field_in_db"]],window[choice_list])
                        td_ele.html(choice_v)
                    }
                    else{
                        td_ele.html(field_v["show_data"])
                    }

                    tr_ele.append(td_ele)
                }
            })
            $("#table_td").append(tr_ele)
        })
    }
    function initchoice(choice_dict) {
        $.each(choice_dict,function (i,j) {
            // a='123'相当于window[a]='123'
            // 这里把choices列表转化为全局变量
            window[i]=j;
        })
    }
    function value_from_choice_list(index,choice) {
        //choice格式:{0: (2) ["male", "男"],}
        //v[0]="male",v[1]="男"
        ret=null
        $.each(choice,function (k,v) {
            if(v[0] === index){
                ret=v[1]
                //js 的return只能跳出当前循环，类似shell的break
                // 所以额外赋值
                return
            }
        })
        return ret
    }
    function DBvalue_from_choice_list(index,choice) {
        //choice格式:{0: (2) ["male", "男"],}
        //v[0]="male",v[1]="男"
        ret=null
        $.each(choice,function (k,v) {
            if(v[1] === index){
                ret=v[0]
                //js 的return只能跳出当前循环，类似shell的break
                // 所以额外赋值
                return
            }
        })
        return ret
    }
    function BindEditMode() {
        $('#EditMode').click(function () {
            //进入编辑模式，应该有个标记，才能区分进入与退出，这里用btn-info属性给button上色
            //所以也用这个属性判断是否在编辑模式，有则是应退出，无则不是应进入
            //也可以自己定义一个属性判断
            if($(this).hasClass("btn-info"))
            {
                OutEditMode()
            }else{
                IntoEditMode()
            }
        })
    }
    function IntoEditMode() {
        $('#EditMode').addClass("btn-info")
        $('#EditMode').text("退出编辑模式")
        //查找checkbox是否选中，有则查找对应tr进入编辑
        $("#table_td").find(":checked").each(function () {
            $cur_tr=$(this).parent().parent()
            TrIntoEdit($cur_tr)
        })
    }
    function OutEditMode() {
        $('#EditMode').removeClass("btn-info")
        $('#EditMode').text("进入编辑模式")
        $("#table_td").find(":checked").each(function () {
            $cur_tr=$(this).parent().parent()
            TrOutEdit($cur_tr)
        })

    }
    function TrIntoEdit(cur_tr) {
        //给当前行加个颜色表示正在编辑
        cur_tr.addClass("info")
        // 标记当前行已编辑，表明可能数据变更，没有则没变更
        cur_tr.attr("has-edit",true)
        // 查找tr下的td含有editable属性的元素进行渲染
        cur_tr.find('[editable="true"]').each(function () {
            var htmllabel = $(this).attr('htmllabel')
            if(htmllabel === 'select'){
                //如果类型是select，获取列表值，渲染成select选择
                var selectData=$(this).attr('selectDataFrom')
                var select_ele=$("<select></select>")
                var cur_select_v=$(this).html()
                $.each(window[selectData],function (select_k,select_v) {
                    var option_ele=$("<option></option>")
                    option_ele.val(select_v[0])
                    option_ele.html(select_v[1])
                    if(cur_select_v === select_v[1]){
                         option_ele.attr("selected",true)
                    }
                   select_ele.append(option_ele)
                })
                $(this).html(select_ele)
            }else {
                label_v=$(this).text()
                input_ele=$("<input>")
                input_ele.val(label_v)
                $(this).html(input_ele)
            }


        })

    }
    function TrOutEdit(cur_tr) {
        //当前行去掉颜色表示退出
        cur_tr.removeClass("info")
        // 查找tr下的td含有editable属性的元素进行渲染
        cur_tr.find('[editable="true"]').each(function () {
            var htmllabel = $(this).attr('htmllabel')
            var selectdata = $(this).attr('selectDataFrom')
            if(htmllabel === 'select'){
                //如果类型是select，获取选中的值，赋值
                var select_ele = $(this).children().first()
                var cur_select_v=select_ele[0].selectedOptions[0].innerHTML
                $(this).html(cur_select_v)
                // 赋新值属性
                origin_v=$(this).attr("origin_v")
                change_v=DBvalue_from_choice_list(cur_select_v,window[selectdata])
                if(origin_v != change_v){
                    $(this).attr("change_v",change_v)
                }
            }else {
                var input_ele = $(this).children().first()
                var cur_input_v=input_ele.val()
                $(this).html(cur_input_v)
                origin_v=$(this).attr("origin_v")
                change_v=cur_input_v
                if(origin_v != change_v){
                    $(this).attr("change_v",change_v)
                }
            }


        })

    }
    function BindCheckboxEditMode() {
        // IntoEditMode的函数有个bug，如果先进入编辑模式，再点击checkbox按钮
        // 当前行不会进入编辑模式，这是因为点击button比勾选快
        // 所以需要对CheckBox进行编辑模式下的事件委托
        $("#table_td").on('click',':checkbox',function () {
            if ($("#EditMode").hasClass("btn-info")) {
                cur_status = $(this).prop('checked');
                var $cur_tr = $(this).parent().parent();
                if(cur_status){
                    TrIntoEdit($cur_tr)
                }else{
                    TrOutEdit($cur_tr)
                }
            }
        })
    }
    function BindSelectAll() {
        // 全选分两种，编辑模式下，要TrIntoEdit,普通则勾选即可
        $('#SelectAll').click(function () {
            // 全选只需处理未被选中的即可
            $("#table_td").find(":checkbox").not(":checked").each(function () {
                if($("#EditMode").hasClass("btn-info")){
                    $(this).prop('checked',true);
                    var $cur_tr = $(this).parent().parent();
                    TrIntoEdit($cur_tr)
                }else{
                    $(this).prop('checked',true);
                }
            })
        })
    }
    function BindReserve() {
        // 反选需要两种情况，编辑模式下，如果选中则TrOutEdit，未选中则TrIntoEdit
        // 普通则反选即可
        $('#Reserve').click(function () {
            $("#table_td").find(":checkbox").each(function () {
                if($("#EditMode").hasClass("btn-info")){
                    var $cur_tr = $(this).parent().parent();
                    if($(this).prop('checked')){
                        $(this).prop('checked',false);
                        TrOutEdit($cur_tr)
                    }else{
                        $(this).prop('checked',true);
                        TrIntoEdit($cur_tr)
                    }

                }else{
                    if($(this).prop('checked')){
                        $(this).prop('checked',false);
                    }
                    else{
                        $(this).prop('checked',true);
                    }
                }
            })
        })
    }
    function BindCancel() {
        // 取消跟全选相反，只需要处理选中的checkbox
        // 也是两种情况，若编辑模式，则TrOutEdit，否则去掉勾选即可
        $('#Cancel').click(function () {
            $("#table_td").find(":checked").each(function () {
                if($("#EditMode").hasClass("btn-info")){
                    $(this).prop('checked',false);
                    var $cur_tr = $(this).parent().parent();
                    TrOutEdit($cur_tr)
                }else{
                    $(this).prop('checked',false);
                }
            })
        })
    }
    function BindSave() {
        // 收集改变的行，每行为一条记录，从tr标签读取旧数据id
        // 从td读取field_name作为key，读取chang_v为value,若无则不赋值
        $('#Save').click(function () {
            // 如果编辑模式下，相当于点了取消
            $('#Cancel').click()
            // 用update_list作为标记，告知后端传送的是更新的数据
            var update_list=[]
            $('#table_td').find('tr[has-edit="true"]').each(function () {
                record={}
                id_v=$(this).attr("old_data_id")
                record["id"]=id_v
               $(this).children('[editable="true"]').each(function(){
                   if($(this).attr("change_v")) {
                       field_k = $(this).attr("field_in_db")
                       field_v = $(this).attr("change_v")
                       record[field_k] = field_v
                   }
                })
                update_list.push(record);
            })
            $.ajax({
                url: requestURL,
                type: 'POST',
                data: {'update_list': JSON.stringify(update_list)},
                dataType: 'json',
                success:function (arg) {
                    if(arg.status=='ok'){
                        initTbody(1)
                    }
                }
            })
        })
    }
    function BindDel() {
        // 删除按钮要获取当前选中行的数据库id，还要弹窗提示确认
        $('#Del').click(function () {
            del_list=[]
            $('#table_td').find(":checked").each(function () {
                record={}
                // save找的是tr，这里是td，所以需parent
                id_v=$(this).parent().parent().attr("old_data_id")
                if(id_v!=undefined) {
                    record["id"] = id_v
                    del_list.push(record)
                }
            })
            var r=confirm("确定删除？");
            if(r){
                $.ajax({
                url: requestURL,
                type: 'POST',
                data: {'del_list': JSON.stringify(del_list)},
                dataType: 'json',
                success:function (arg) {
                    if(arg.status=='ok'){
                        initTbody(1)
                    }
                }
             })
            }
        })
    }
    jQuery.extend({
        'CreateCURD':function (url) {
                    requestURL = url;
                    initTable(1);
                    BindEditMode();
                    BindCheckboxEditMode();
                    BindSelectAll();
                    BindCancel();
                    BindReserve();
                    BindSave();
                    BindDel();
                },
        'TurnToPager':function (num) {
                    inittable(num);
                }
            })
    })