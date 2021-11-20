import * as React from 'react';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import StorageIcon from '@mui/icons-material/Storage';
import PublicIcon from '@mui/icons-material/Public';

export const DataSelection = ({selectedIndex, onClick}) => {
  
  return (
    <Box sx={{ width: '100%', maxWidth: 360, bgcolor: 'background.paper' }}>
      <List component="nav" aria-label="main mailbox folders">
        <ListItemButton
          selected={selectedIndex === 'location'}
          onClick={() => onClick('location')}
        >
          <ListItemIcon>
            <StorageIcon style={{width:20, height:20}}/>
          </ListItemIcon>
          <ListItemText secondary="CCG to Region" />
        </ListItemButton>
        <ListItemButton
          selected={selectedIndex === 'lsoa'}
          onClick={() => onClick('lsoa')}
        >
          <ListItemIcon>
            <StorageIcon style={{width:20, height:20}} />
          </ListItemIcon>
          <ListItemText secondary="LSOA to Region" />
        </ListItemButton>
        <ListItemButton
          selected={selectedIndex === 'trustGeodata'}
          onClick={() => onClick('trustGeodata')}
        >
          <ListItemIcon>
            <PublicIcon style={{width:20, height:20}}/>
          </ListItemIcon>
          <ListItemText secondary="All trusts geodata" />
        </ListItemButton>
      </List>
      <Divider />
    </Box>
  );
}
