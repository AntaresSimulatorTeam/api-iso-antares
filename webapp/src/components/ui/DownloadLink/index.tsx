/* eslint-disable jsx-a11y/click-events-have-key-events */
/* eslint-disable jsx-a11y/no-static-element-interactions */
import React, { ReactNode } from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { addDownload } from '../../../ducks/download';

const mapState = () => ({
});

const mapDispatch = ({
  download: addDownload,
});

const connector = connect(mapState, mapDispatch);
type PropsFromRedux = ConnectedProps<typeof connector>;

interface OwnProps {
  url: string;
  name: string;
  children?: ReactNode;
}
type PropTypes = PropsFromRedux & OwnProps;

const DownloadLink = (props: PropTypes) => {
  const { children, name, url, download } = props;

  const handleClick = async () => {
    download({ url, name });
  };

  return (
    <span onClick={handleClick}>
      {children}
    </span>
  );
};

export default connector(DownloadLink);
