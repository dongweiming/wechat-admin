<template>
	<section>
    <div class="wx-text">
    <label class="el-form-item__label">欢迎文本</label>
    <el-input type="textarea" :rows="2" style="width: 500px;" v-model="welcome_text">
    </el-input>
    </div>
    <div class="wx-text">
    <label class="el-form-item__label">邀请文本</label>
    <el-input type="textarea" :rows="4" style="width: 500px;" v-model="invite_text">
    </el-input>
    </div>
    <div class="wx-text">
    <label class="el-form-item__label">新群模板</label>
    <el-input style="width: 500px;" v-model="group_tmpl">
    </el-input>
    </div>
    <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="users" :data="allMembers" :titles="['好友列表', '已选好友']">
    </el-transfer>
    <div class="save-btn">
      <el-button @click="saveSettings" type="primary" :loading="saveLoading">保存设置</el-button>
    </div>
	</section>
</template>

<script>
  import { getGroupSetings, updateGroupSetings } from '../../api/api'; 
	export default {
		data() {
      return {
        allMembers: [],
        users: [],
        welcome_text: '',
        invite_text: '',
        group_tmpl: '',
        saveLoading: false,
        filterMethod(query, item) {
          return item.label.indexOf(query) > -1;
        },
        default: {
            welcome_text: '🎉 欢迎 @{} 的加入！',
            invite_text: `欢迎您！
请输入关键字 Python 加入群：                                            

进群四件事：

1、阅读群公告，
2、修改群名片，
3、做自我介绍，
4、要是发红包，总额请不要低于50
                                                                                       
请言行遵守群内规定，违规者将受到处罚，拉入黑名单。`,
            'group_tmpl': 'Python✌{}群'
        }
      };
		},
		methods: {
      getMembers () {
        const users = [], creators = [];
 
         getGroupSetings().then((res) => {
           res.data.users.forEach((member, index) => {
             users.push({
               label: member.nick_name,
               key: member.id
             });
           });
           this.allMembers = users;
           this.users = res.data.creators;
           this.welcome_text = res.data.welcome_text || this.default.welcome_text;
           this.invite_text = res.data.invite_text || this.default.invite_text;
           this.group_tmpl = res.data.group_tmpl || this.default.group_tmpl;
         });
      },
      saveSettings () {
        let para = {
            'welcome_text': this.welcome_text,
            'invite_text': this.invite_text,
            'group_tmpl': this.group_tmpl,
            'creators': this.users
        };
        this.saveLoading = true;
        updateGroupSetings(para).then((res) => {
            this.$notify({
             title: 'Success',
             message: '更新建群成员设置成功',
             type: 'success'
           });
           this.saveLoading = false;
        });
      },
    },
		mounted() {
			this.getMembers();
		}
	}

</script>

<style scoped>
.wx-text {
  margin-bottom: 20px;
}
.save-btn {
  margin-top: 30px;
  text-align: center;
}
</style>