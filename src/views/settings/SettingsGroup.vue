<template>
	<section>
    <desc-block>
      <div slot="wx" class="wx-item">
        <label class="el-form-item__label">欢迎文本</label>
        <el-input type="textarea" :rows="2" style="width: 500px;" v-model="welcome_text">
        </el-input>
      </div>
      <div slot="desc">
        <p>设置进群的欢迎语句</p>
      </div> 
    </desc-block>
    <desc-block>
      <div slot="wx" class="wx-item"> 
        <label class="el-form-item__label">邀请文本</label>
        <el-input type="textarea" :rows="4" style="width: 500px;" v-model="invite_text">
        </el-input>
      </div>
      <div slot="desc">
         <p>文本中可提及加群的关键词策略，比如包含<code>python</code>可以进入Python技术群；也可作为群公告使用</p>
      </div>
    </desc-block>
    <desc-block>
      <div slot="wx" class="wx-item"> 
        <p class="rule-header">建群设置</p> 
        <div class="rule-wrapper el-textarea">
          <div class="rule" v-for="(p, index) in group_patterns">
            <label class="rule-label">模式</label>
            <el-input style="width: 200px;" v-model="p[0]"></el-input>
            <label class="rule-label">群模板</label>
            <el-input style="width: 200px;" v-model="p[1]"></el-input>
            <el-button size="small" type="danger" @click.prevent="removeRule(p)" v-if="index >= 1">删除规则</el-button>
          </div>
        </div>
        <el-button type="info" @click="addRule">新增规则</el-button>
      </div>
      <div slot="desc">
        <p>配置上面提及的加群的关键词策略，模式输入框支持正则表达式，模板需要保留一个<code>{}</code>，这是Python format的需要，数字默认是1，下一个群是2，以此类推</p>
      </div>
    </desc-block>
    <desc-block>
      <div slot="wx" class="wx-item">
        <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="users" :data="allMembers" :titles="['好友列表', '已选好友']">
        </el-transfer>
        <div class="save-btn">
          <el-button @click="saveSettings" type="primary" :loading="saveLoading">保存设置</el-button>
        </div>
      </div>
      <div slot="desc">
        <p>自动创建新群需要至少3个好友，这里需要从<code>好友列表</code>中选择还有放入右侧的<code>已选好友</code>列表中。不选择的话新群创建无法成功！</p>
      </div>
    </desc-block>
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
.wx-item {
  padding: 10px 0 10px 10px;
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
  padding: 20px 0;
  width: 620px;
  margin-left: -11px;
}
.rule-header {
  color: #48576a;
}
</style>