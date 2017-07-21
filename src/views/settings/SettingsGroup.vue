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
    <label class="el-form-item__label">建群设置</label> 
    <div class="wx-text rule-wrapper el-textarea">
      <div class="rule" v-for="(p, index) in group_patterns">
        <label class="rule-label">模式</label>
        <el-input style="width: 200px;" v-model="p[0]"></el-input>
        <label class="rule-label">群模板</label>
        <el-input style="width: 200px;" v-model="p[1]"></el-input>
        <el-button type="danger" @click.prevent="removeRule(p)" v-if="index >= 1">删除规则</el-button>
      </div>
    <el-button type="info" @click="addRule">新增规则</el-button>
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
        group_patterns: {},
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
           this.group_patterns = res.data.group_patterns;
         });
      },
      saveSettings () {
        let para = {
            'welcome_text': this.welcome_text,
            'invite_text': this.invite_text,
            'group_patterns': this.group_patterns,
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
      removeRule(item) {
        var index = this.group_patterns.indexOf(item)
        if (index !== -1) {
          this.group_patterns.splice(index, 1)
        }
      },
      addRule() {
        let p = this.group_patterns[this.group_patterns.length - 1];
        if (!p[0] || !p[1]) {
          this.$message.error('先完成现有的哦😯');
          return
        }
        this.group_patterns.push(['', '']);
      }
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
.rule {
  margin-bottom: 12px;
}
.rule-label {
  text-align: right;
  vertical-align: middle;
  font-size: 14px;
  color: #48576a;
  line-height: 1;
  padding: 11px;
  box-sizing: border-box;
}
.rule-wrapper {
  padding: 20px;
  border: 1px solid #bfcbd9;
  width: 620px;
}
</style>