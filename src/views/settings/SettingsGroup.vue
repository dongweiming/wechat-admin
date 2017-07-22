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
            <el-button size="small" type="danger" @click.prevent="removeRule(p, group_patterns)" v-if="index >= 1">删除规则</el-button>
          </div>
        </div>
        <el-button type="info" @click="addRule('group_patterns')">新增规则</el-button>
      </div>
      <div slot="desc">
        <p>配置上面提及的加群的关键词策略，模式输入框支持正则表达式，模板需要保留一个<code>{}</code>，这是Python format的需要，数字默认是1，下一个群是2，以此类推</p>
      </div>
    </desc-block>
    <desc-block>
      <div slot="wx" class="wx-item">
        <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="users" :data="allMembers" :titles="['好友列表', '已选好友']">
        </el-transfer>
      </div>
      <div slot="desc">
        <p>自动创建新群需要至少3个好友，这里需要从<code>好友列表</code>中选择还有放入右侧的<code>已选好友</code>列表中。不选择的话新群创建无法成功！</p>
      </div>
    </desc-block>
    <desc-block>
      <div slot="wx" class="wx-item">
        <p class="rule-header">公众号转发群聊设置</p> 
        <div class="rule-wrapper el-textarea">
          <div class="rule" v-for="(p, index) in mp_forward">
            <label class="rule-label">公众号</label>
            <el-select v-model="p[0]" clearable placeholder="请选择公众号">
              <el-option v-for="item in mps" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <label class="rule-label">群聊</label>
            <el-select v-model="p[1]" multiple placeholder="请选择群聊">
              <el-option v-for="item in groups" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
            <el-button size="small" type="danger" @click.prevent="removeRule(p, mp_forward)" v-if="index >= 1">删除规则</el-button>
          </div>
        </div>
        <el-button type="info" @click="addRule('mp_forward')">新增规则</el-button>
      </div>
      <div slot="desc">
        <p>每个公众号发送的文章可转发到多个群聊中，规则可选择多条</p>
      </div>
    </desc-block>
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
        mps: [],
        groups: [],
        users: [],
        welcome_text: '',
        invite_text: '',
        group_patterns: [],
        mp_forward: [],
        saveLoading: false,
        filterMethod(query, item) {
          return item.label.indexOf(query) > -1;
        }
      };
		},
		methods: {
      getData () {
        const users = [], mps = [], groups = [];
 
         getGroupSetings().then((res) => {
           res.data.users.forEach((member, index) => {
             users.push({
               label: member.nick_name,
               key: member.id
             });
           });
           res.data.groups.forEach((member, index) => {
             groups.push({
               label: member.nick_name,
               value: member.id
             });
           });
           res.data.mps.forEach((member, index) => {
             mps.push({
               label: member.nick_name,
               value: member.id
             });
           });
           this.allMembers = users;
           this.users = res.data.creators;
           this.welcome_text = res.data.welcome_text;
           this.invite_text = res.data.invite_text;
           this.group_patterns = res.data.group_patterns;
           this.mp_forward = res.data.mp_forward || [];
           this.mps = mps;
           this.groups = groups;
         });
      },
      saveSettings () {
        let para = {
            'welcome_text': this.welcome_text,
            'invite_text': this.invite_text,
            'group_patterns': this.group_patterns,
            'creators': this.users,
            'mp_forward': this.mp_forward
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
      removeRule(item, items) {
        var index = items.indexOf(item)
        if (index !== -1) {
          items.splice(index, 1)
        }
      },
      addRule(items) {
        let len = this[items].length, newItem;
        if (len) {
          let p = this[items][len - 1];
          if (!p[0] || !p[1]) {
            this.$message.error('先完成现有的哦😯');
            return
          }
        }
        if (items === 'mp_forward') {
          if (!this.mps.length) {
            this.$message.error('你并没有关注公众号😯');
            return
          }
          if (!this.groups.length) {
            this.$message.error('你并没有加入群聊😯');
            return
          } 
          newItem = ['', []];
        } else {
          newItem = ['', ''];
        }
        this[items].push(newItem);
      }
    },
		mounted() {
			this.getData();
		}
	}

</script>

<style scoped>
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
section {
  margin-top: 20px;
}
</style>