import axios from 'axios';

let base = `${API_URL}/j`;

const request = (url, options={}, method='get') => {
    let key = ~['delete', 'get', 'head'].indexOf(method) ? 'params' : 'data';
    return axios(Object.assign({'url': url, 'method':method, 'validateStatus': false}, {[key]: options})).then(
        res => res);
}

const requestLogin = () => {
    return request(`${base}/login`, {}, 'post');
};

const requestLogout = () => {
    return request(`${base}/logout`, {}, 'post');
};

const getUserList = params => {
    return request(`${base}/users`, params);
}

const getGroupSetings = _ => {
    return request(`${base}/settings/group`);
}

const updateGroupSetings = params => {
    return request(`${base}/settings/group`, params, 'put');
}

const getGroupList = params => {
    return request(`${base}/groups`, params);
}

const removeUser = (id, params) => {
    return request(`${base}/user/${id}`, params, 'delete');
}

const removeGroup = id => {
    return request(`${base}/group/${id}`, {}, 'delete');
}

const batchRemoveUser  = params => {
    return request(`${base}/users`, params, 'delete');
}

const batchRemoveGroup  = params => {
    return request(`${base}/groups`, params, 'delete');
}

const addUser = params => {
    return request(`${base}/user/${params.wxid}`, params, 'put');
}

const addUsers = params => {
    return request(`${base}/users`, params, 'put');
}

const addGroup = params => {
    return request(`${base}/groups`, params, 'put');
}

const getAllUsers = () => {
    return request(`${base}/all_users`);
}

const sendMessage = params => {
    return request(`${base}/send_message`, params, 'post');
}

const getAllGroups = () => {
    return request(`${base}/all_groups`);
}

const getMsgList = params => {
    return request(`${base}/messages`, params);
}

const readAll = () => {
    return request(`${base}/readall`, {}, 'post');
}

module.exports = {
    requestLogin,
    requestLogout,
    getUserList,
    removeUser,
    addUser,
    addUsers,
    batchRemoveUser,
    getGroupList,
    batchRemoveGroup,
    removeGroup,
    getAllUsers,
    getGroupSetings,
    updateGroupSetings,
    sendMessage,
    getAllGroups,
    addGroup,
    getMsgList,
    readAll,
    API_URL
};
