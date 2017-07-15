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
           this.welcome_text = res.data.welcome_text;
           this.invite_text = res.data.invite_text;
           this.group_tmpl = res.data.group_tmpl;
         });
      },
      saveSettings () {
        let para = {
            'welcome_text': this.welcome_text,
            'invite_text': this.invite_text,
            'group_tmpl': this.group_tmpl,
            'creators': this.users,
        };
        this.saveLoading = true;
        updateGroupSetings(para).then((res) => {
            this.$notify({
             title: 'Success',
             message: '更新群聊设置成功',
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