import Login from './views/Login.vue'
import NotFound from './views/404.vue'
import Home from './views/Home.vue'
import Main from './views/Main.vue'

import Contact from './views/users/Contact.vue'
import Group from './views/groups/Group.vue'
import GroupMember from './views/groups/GroupMember.vue'
import SendMsgToContact from './views/users/SendMsgToContact.vue'
import SendMsgToGroup from './views/groups/SendMsgToGroup.vue'
import SettingsGroup from './views/settings/SettingsGroup.vue'

let routes = [
    {
        path: '/login',
        component: Login,
        name: '',
        hidden: true
    },
    {
        path: '/404',
        component: NotFound,
        name: '',
        hidden: true
    },
    {
        path: '/',
        component: Home,
        name: '主页',
        iconCls: 'fa fa-address-card',
        leaf: true,
        children: [
            { path: '/main', component: Main, name: '主页', iconCls: 'el-icon-message' }
        ]
    },
    {
        path: '/',
        component: Home,
        name: '用户',
        iconCls: 'el-icon-message',
        children: [
            { path: '/contact', component: Contact, name: '联系人列表' },
            { path: '/send_msg/contact', component: SendMsgToContact, name: '群发消息' },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '群组',
        iconCls: 'fa fa-id-card-o',
        children: [
            { path: '/groups', component: Group, name: '我的群聊' },
            { path: '/send_msg/group', component: SendMsgToGroup, name: '发群消息' },
            { path: '/group/:id', component: GroupMember, name: '群聊成员列表', hidden: true },
        ]
    },
    {
        path: '/',
        component: Home,
        name: '设置',
        iconCls: 'fa fa-id-card-o',
        children: [
            { path: '/settings/group', component: SettingsGroup, name: '群聊设置' },
        ]
    },
    {
        path: '*',
        hidden: true,
        redirect: { path: '/404' }
    }
];

export default routes;
