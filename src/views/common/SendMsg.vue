<template>
  <div>
  <el-input
      type="textarea"
      :autosize="{ minRows: 5, maxRows: 10}"
      placeholder="请输入内容"
      v-model="content" contenteditable="true">
    </el-input>
  <div class="icon clearfix">
      <i class="icon iconfont icon-face" @click="showEmoji = !showEmoji"></i>
      <transition name="fade" mode="">
        <div class="emoji-box" v-if="showEmoji" >
          <el-button
            class="pop-close"
            :plain="true"
            type="danger"
            size="mini"
            icon="close"
            @click="showEmoji = false"></el-button>
            <vue-emoji
              @select="selectEmoji">
            </vue-emoji>
          <span class="pop-arrow arrow"></span>
        </div>
      </transition>
    </div>
    <el-dialog title="发送消息" :visible.sync="dialogVisible">
      <h4>你输入的内容是：</h4>
      <p v-html="emoji(content)" class="content"></p>
      <h4>选择要发送的好友：</h4>
      <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="users" :data="allMembers" :titles="['好友列表', '已选好友']">
      </el-transfer>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submit">确 定</el-button>
      </div>
    </el-dialog>
    <el-button type="success" @click="dialogVisible = true" class="submit">提交</el-button>
    </div>
  </div>

</template>

<script>
  import '../../plugins/emoji/src/assets/css/iconfont.css'
  import vueEmoji from '../../plugins/emoji/src/components/emoji.vue'
  import { getUserList, getAllGroups, sendMessage } from '../../api/api';

	export default {
		data() {
      return {
        originalContent: '',
        content: '',
        showEmoji: false,
        dialogVisible: false,
        users: [],
        allMembers: [],
        filterMethod(query, item) {
           return item.label.indexOf(query) > -1;
        },
      }
		},
    props: ['queryType', 'gid'],
		methods: {
      getMembers () {
         const users = [];
         let para = {
           gid: this.gid || '',
           page: 0,
           q: '',
           type: this.queryType
         };
         getUserList(para).then((res) => {
            res.data.users.forEach((member, index) => {
              users.push({
                label: member.nick_name,
                key: member.id
              });
            });
            this.allMembers = users;
          });
      },
      selectEmoji (code) {
        let emoji = code.slice(1, -1);
        this.showEmoji = false
        this.content += code
        this.originalContent += `[${ emoji.replace(/\b\w/g, l => l.toUpperCase()) }]`;
      },
      submit () {
        this.dialogVisible = false
        this.originalContent = ''
        this.content = ''
        let para = {
          type: this.queryType,
          gid: this.gid || '',
          content: this.originalContent,
          ids: this.users
        }
        sendMessage(para).then((res) => {
            this.listLoading = false;
            this.$checkStatus(res);
            this.getUsers();
          });
      }
		},
    components: {
      vueEmoji
    },
    mounted() {
      this.getMembers();
    }
	}

</script>

<style lang="scss" scoped>
ul{
  margin: 0;
  padding: 0;
  list-style: none;
}
.el-dialog__title {
  font-size: 18px;
}
.icon {
  position: relative;
  margin-top: 20px;
  .iconfont {
    cursor: pointer;
    color: #F7BA2A;
  }
  .emoji-box {
    position: absolute;
    z-index: 10;
    left: -10px;
    top: 24px;
    box-shadow: 0 4px 20px 1px rgba(0, 0, 0, 0.2);
    background: white;
    .el-button {
      position: absolute;
      border: none;
      color: #FF4949;
      right: 12px;
      top: 12px;
      z-index: 10;
    }
    .arrow {
      left: 10px;
    }
  }
  .submit {
    float: right;
  }
}
.comment {
  margin-top: 20px;
  .item {
    margin-top: 20px;
    padding: 10px;
    margin: 0;
    border-top: 1px solid #bfcbd9;
  }
}
.clearfix {
  &:after {
    content: '';
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
  }
}
.fade-enter-active, .fade-leave-active { transition: opacity .5s; }
.fade-enter, .fade-leave-active { opacity: 0; }
.fade-move { transition: transform .4s; }
.list-enter-active, .list-leave-active { transition: all .5s; }
.list-enter, .list-leave-active { opacity: 0; transform: translateX(30px); }
.list-leave-active { position: absolute !important; }
.list-move { transition: all .5s;}
h4, .content {
  margin-bottom: 20px;
}
.content {
  border: 1px solid #eaeefb;
  padding: 10px;
}
.el-button--success {
  margin-top: 20px;
}
</style>