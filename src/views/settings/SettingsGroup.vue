<template>
	<section>
    <el-transfer filterable :filter-method="filterMethod" filter-placeholder="请输入好友昵称" v-model="users" :data="allMembers" :titles="['好友列表', '已选好友']" @change="handleChange">
    </el-transfer>
	</section>
</template>

<script>
  import { getGroupSetings, updateGroupSetings } from '../../api/api'; 
	export default {
		data() {
      return {
        allMembers: [],
        users: [],
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
         });
      },
      handleChange (value, direction, movedKeys) {
        updateGroupSetings({'creators': this.users}).then((res) => {
          this.$notify({
            title: 'Success',
            message: '更新建群成员设置成功',
            type: 'success'
          });
        });
      }
		},
		mounted() {
			this.getMembers();
		}
	}

</script>

<style scoped>

</style>